import asyncio
import aiohttp
import py_nillion_client as nillion
import os

from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")


async def fetch_player_alias():
    url = "http://localhost:5000/get-player"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['player_alias']
            else: 
                print(f"Failed to get player alias: {response.status}")
                return None
            
async def fetch_secrets():
    url = "http://localhost:5000/get-secret"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"FAILED TO RETRIVE SECRETS: {response.status}")
                return None
            

async def main(): 
    
    PLAYER_ALIAS = await fetch_player_alias()
    if PLAYER_ALIAS:
        print(f"Player alias retrieved: {PLAYER_ALIAS}")
        # Now you can use PLAYER_ALIAS in the rest of your logic
    else:
        print("Could not retrieve PLAYER_ALIAS")
    
    
    MANAGER = "GAME_MANAGER"
    
    # PLAYER
    seed = PLAYER_ALIAS
    user_key = UserKey.from_seed(seed)
    node_key = NodeKey.from_seed(seed)
    PLAYER_CLIENT = create_nillion_client(user_key, node_key)
    
    manager_seed = MANAGER
    user_key = UserKey.from_seed(manager_seed)
    node_key = NodeKey.from_seed(manager_seed)
    MANAGER_CLIENT = create_nillion_client(user_key, node_key)
    
    player_user_id = PLAYER_CLIENT.user_id
    player_party_id = PLAYER_CLIENT.party_id
    
    manager_user_id = MANAGER_CLIENT.user_id
    manager_party_id = MANAGER_CLIENT.party_id
    
    # GET NILLION-DEVNET CREDENTIALS
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
       
    # CREATE THE PAYMENTS CONFIG, SET UP NILLION WALLET etc.
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )
    
    # DEPLOY THE PROGRAM BY GAME MANAGER
    
    CHECK_EQUAL_PROGRAM = "check_equal"
    PROGRAM_PATH = f"../nada_quickstart_programs/target/{CHECK_EQUAL_PROGRAM}.nada.bin"
    
    check_equal_program_receipt = await get_quote_and_pay(
        MANAGER_CLIENT,
        nillion.Operation.store_program(PROGRAM_PATH),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    action_id = await MANAGER_CLIENT.store_program(
        cluster_id, CHECK_EQUAL_PROGRAM, PROGRAM_PATH, check_equal_program_receipt
    )
    
    PROGRAM_ID = f'{manager_user_id}/{CHECK_EQUAL_PROGRAM}'
    
    # DEPLOY THE SECRETS 

    SECRETS = await fetch_secrets()

    secret_guess = SECRETS['secret_guess']
    secret_target = SECRETS['secret_target']

    SECRET_GUESS = nillion.NadaValues(
        {
            "SECRET_GUESS": nillion.SecretInteger(secret_guess),
        }
    )
    permissions = nillion.Permissions.default_for_user(player_user_id)    
    permissions.add_compute_permissions({PLAYER_CLIENT.user_id: {PROGRAM_ID}})
    permissions.add_compute_permissions({MANAGER_CLIENT.user_id: {PROGRAM_ID}})
    
    receipt_store = await get_quote_and_pay(
        PLAYER_CLIENT,
        nillion.Operation.store_values(SECRET_GUESS, ttl_days=5),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    guess_store_id = await PLAYER_CLIENT.store_values(
        cluster_id, SECRET_GUESS, permissions, receipt_store
    )
    
    SECRET_TARGET = nillion.NadaValues(
        {
            "SECRET_TARGET": nillion.SecretInteger(secret_target),
        }
    )
    permissions = nillion.Permissions.default_for_user(manager_user_id)    
    permissions.add_compute_permissions({PLAYER_CLIENT.user_id: {PROGRAM_ID}})
    permissions.add_compute_permissions({MANAGER_CLIENT.user_id: {PROGRAM_ID}})
    
    receipt_store = await get_quote_and_pay(
        MANAGER_CLIENT,
        nillion.Operation.store_values(SECRET_TARGET, ttl_days=5),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    target_store_id = await MANAGER_CLIENT.store_values(
        cluster_id, SECRET_TARGET, permissions, receipt_store
    )
            
    # SET UP COMPUTATION OF THE SECRETS
    compute_bindings = nillion.ProgramBindings(PROGRAM_ID)
    compute_bindings.add_input_party(PLAYER_ALIAS, player_party_id)  # Ensure the correct input party is added
    compute_bindings.add_input_party(MANAGER, manager_party_id)  # Add Game Manager as input party
    compute_bindings.add_output_party(MANAGER, manager_party_id)

    COMPUTE_SECRETS = nillion.NadaValues({})

    receipt_compute = await get_quote_and_pay(
        MANAGER_CLIENT,
        nillion.Operation.compute(PROGRAM_ID, COMPUTE_SECRETS),
        payments_wallet,
        payments_client,
        cluster_id
    )

    compute_id = await MANAGER_CLIENT.compute(
        cluster_id,
        compute_bindings,
        [guess_store_id, target_store_id],
        COMPUTE_SECRETS,
        receipt_compute
    )

    print(f"BLIND COMPUTATION COMPLETE: {compute_id}")

    # RETURN THE COMPUTATION RESULTS
    print(f"THE COMPUTATION WAS SENT TO THE NETWORK -> ID: {compute_id}")
    while True:
        compute_event = await MANAGER_CLIENT.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"🖥️  The result is: {compute_event.result.value}")
            return compute_event.result.value    
    
if __name__ == "__main__":
    asyncio.run(main())
