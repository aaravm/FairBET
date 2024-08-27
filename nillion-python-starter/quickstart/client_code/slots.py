import asyncio
import py_nillion_client as nillion
import os

import psutil
import platform 
import subprocess
import hashlib
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
    return {"PLAYERS":{}}


async def main(): 
    
    # FIXME: TO BE EXTRACTED FROM THE FRONTEND
    PLAYER_ALIAS = "User"
    
    # GET NILLION-DEVNET CREDENTIALS
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    
    seed = PLAYER_ALIAS
    user_key = UserKey.from_seed(seed)
    node_key = NodeKey.from_seed(seed)
    
    player = create_nillion_client(user_key, node_key)
    
    party_id = player.party_id
    user_id = player.user_id    
    
    # CREATE THE PAYMENTS CONFIG, SET UP NILLION WALLET etc.
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )
    
    # DEPLOY THE PROGRAM 
    PROGRAM_NAME="check_equal"
    PROGRAM_PATH = f"../nada_quickstart_programs/target/{PROGRAM_NAME}.nada.bin"
    
    PROGRAM_ID = f'{user_id}/{PROGRAM_NAME}'

    GAME_MANAGER = "Game Manager"

    seed = GAME_MANAGER
    user_key = UserKey.from_seed(seed)
    node_key = NodeKey.from_seed(seed)
    
    game_manager = create_nillion_client(user_key, node_key)
    
    game_manager_party_id = game_manager.party_id
    game_manager_user_id = game_manager.user_id    

    # TODO: Get secret_guess and secret_target from frontend
    secret_guess=10
    secret_target=10

    RESULT= nillion.NadaValues(
        {
            "secret_guess": nillion.SecretInteger(secret_guess),
            "secret_target": nillion.SecretInteger(secret_target)
        }
    )
    print(RESULT)
    permissions = nillion.Permissions.default_for_user(player.user_id)    
    permissions.add_compute_permissions({player.user_id: {PROGRAM_ID}})
    
    receipt_store = await get_quote_and_pay(
        player,
        nillion.Operation.store_values(RESULT, ttl_days=5),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    store_id = await player.store_values(
        cluster_id, RESULT, permissions, receipt_store
    )
        
    print(f"SERIAL NUMBER AND WALLET ADDRESS STORED: {store_id}")
    
    # SET UP COMPUTATION OF THE SECRETS
    compute_bindings = nillion.ProgramBindings(PROGRAM_ID)
    compute_bindings.add_input_party(PLAYER_ALIAS, party_id)  # Ensure the correct input party is added
    compute_bindings.add_input_party(GAME_MANAGER, game_manager_party_id)  # Add Game Manager as input party
    compute_bindings.add_output_party(GAME_MANAGER, game_manager_party_id)

    COMPUTE_SECRETS = nillion.NadaValues({})

    receipt_compute = await get_quote_and_pay(
        player,
        nillion.Operation.compute(PROGRAM_ID, COMPUTE_SECRETS),
        payments_wallet,
        payments_client,
        cluster_id
    )
    print(f"cluster_id: {cluster_id}")
    print(f"compute_bindings: {compute_bindings}")
    print(f"store_id: {store_id}")
    print(f"COMPUTE_SECRETS: {COMPUTE_SECRETS}")
    print(f"receipt_compute: {receipt_compute}")

    compute_id = await player.compute(
        cluster_id,
        compute_bindings,
        [store_id],
        COMPUTE_SECRETS,
        receipt_compute
    )

    print(f"BLIND COMPUTATION COMPLETE: {compute_id}")

    # RETURN THE COMPUTATION RESULTS
    print(f"THE COMPUTATION WAS SENT TO THE NETWORK -> ID: {compute_id}")
    while True:
        compute_event = await player.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"🖥️  The result is: {compute_event.result.value}")
            return compute_event.result.value
    
    print(f"BLIND COMPUTATION COMPLETE: {compute_id}")
    
    # THE BELOW CODE IS RESUNDANT, WE DONT NEED IT    
    # RETURN THE COMPUTATION RESULTS
    print(f"THE COMPUTATION WAS SENT THE NETWORK -> ID: {compute_id}")
    while True:
        compute_event = await player.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"🖥️  The result is: {compute_event.result.value}")
            return compute_event.result.value
    
    
if __name__ == "__main__":
    asyncio.run(main())
