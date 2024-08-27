import asyncio
import py_nillion_client as nillion
import os
import json

from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

def load_creds(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {"PLAYERS": {}}

def load_player_creds():
    CRED_STORE_PATH = "./credential_store.json"
    creds = load_creds(CRED_STORE_PATH)
    return creds

async def main():
    
    #FIXME: GAME_MANAGER NAME COULD BE RANDOMISED AND EXTRACTED FROM THE FRONTEND
    PLAYER_ALIAS = "GAME_MANAGER"
    
    # GET NILLION-DEVNET CREDENTIALS
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    
    print("CLUSTER_ID: ", cluster_id)
    print(type(cluster_id))
    
    seed = PLAYER_ALIAS
    user_key = UserKey.from_seed(seed)
    node_key = NodeKey.from_seed(seed)
    
    manager = create_nillion_client(user_key, node_key)
    
    party_id = manager.party_id
    user_id = manager.user_id
    
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )
    
    # DEPLOY THE SHUFFLING PROGRAM 
    SHUFFLING_PROGRAM = "random_shuffle"
    SHUFFLING_PROGRAM_PATH = f"../nada_quickstart_programs/target/{SHUFFLING_PROGRAM}.nada.bin"
    
    shuffle_program_receipt = await get_quote_and_pay(
        manager,
        nillion.Operation.store_program(SHUFFLING_PROGRAM_PATH),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    action_id = await manager.store_program(
        cluster_id, SHUFFLING_PROGRAM, SHUFFLING_PROGRAM_PATH, shuffle_program_receipt
    )
    
    PROGRAM_ID = f'{user_id}/{SHUFFLING_PROGRAM}'    
    
    # SET UP THE SHUFFLING COMPUTATION 
    
    compute_bindings = nillion.ProgramBindings(PROGRAM_ID)
    
    # THERE WILL BE NO INPUT BINDINGS
    
    # ADD EXISTING PLAYERS TO THE OUTPUT BINDINGS
    CREDS = load_player_creds()  
    PLAYERS = CREDS["PLAYERS"]
        
    for player_alias, player_info in PLAYERS.items(): 
        print(player_alias, player_info)
        compute_bindings.add_output_party(player_info['party_name'], player_info['party_id'])
        
    compute_bindings.add_output_party(PLAYER_ALIAS, party_id)
    
    COMPUTE_SECRETS = nillion.NadaValues({})
    
    COMPUTE_RECEIPT = await get_quote_and_pay(
        manager,
        nillion.Operation.compute(PROGRAM_ID, COMPUTE_SECRETS),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    COMPUTE_ID = await manager.compute(
        cluster_id,
        compute_bindings,
        [],
        COMPUTE_SECRETS,
        COMPUTE_RECEIPT
    )
    
    print("BLIND RANDOMIZED SHUFFLING COMPLETE: ", COMPUTE_ID)

if __name__ == "__main__":
    asyncio.run(main())
