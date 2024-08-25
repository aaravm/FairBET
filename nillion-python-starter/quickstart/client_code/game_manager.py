# BASICALLY WHAT WE ARE DOING IS WE ARE INITIATING A PLAYER CLIENT IN THE DEVNET 
# Then we push the Player's system credentials and wallet address in a .env file,
# Then these credentials are extracted by the game_manager in its client code and then 
# these credentials are computed blindly in the network and the final 
# UNIFIED_SYSTEM_IDENTIFIER FOR HARDWARE BAN is computed in the network 
# and stored under the ownership of the game_manager

# now he can see if that UNIFIED_SYSTEM_IDENTIFIER FOR HARDWARE BAN is BANNED OR NOT, 
# and hence HARWARE_BANNING could be implemented

import asyncio
import py_nillion_client as nillion
import os

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

# FIXME: GET THIS FUNCTION IN A UTILS FILE 
def string_to_int(s):
    hash_object = hashlib.sha256(s.encode())    # USE SHA256 HASH FUNCTION
    hex_dig = hash_object.hexdigest()           # GET HEXADECIMAL DIGEST
    return int(hex_dig,  16)                    # CONVERT HEX TO INTEGER 
    
async def main():
    
    # GET NILLION-DEVNET CREDENTIALS
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    
    seed = "GAME_MANAGER"
    user_key = UserKey.from_seed(seed)
    node_key = NodeKey.from_seed(seed)
    
    manager = create_nillion_client(user_key, node_key)
    
    party_id = manager.party_id
    user_id = manager.user_id
    
    # PARTY NAMES WE NEED SO TO SPECIFY WHICH CLIENT IS GIVING THE INPUTS AND RECEIVING THE OUTPUTS
    GAME_MANAGER_PARTY = "GAME_MANAGER"
    
    with open("credential_store.json", "r") as f:
        game = json.load(f)
        PLAYER_INFO = game["PLAYER1"]
    
    # CREATE THE PAYMENTS CONFIG, SET UP NILLION WALLET etc.
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )
    
    get_sn = "addition"
    get_sn_path = f"../mada_quickstart_programs/target/{get_sn}.nada.bin"
    
    # DEPLOY THE COMPUTATION PROGRAM UNDER THE OWNERSHIP OF GAME_MANAGER
    receipt_store_program = await get_quote_and_pay(
        manager,
        nillion.Operation.store_program(get_sn_path),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    action_id = await manager.store_program(
        cluster_id, get_sn, get_sn_path, receipt_store_program
    )
    
    # NOW WE CREATE A VARIABLE FOR THE PROGRAM ID TO SET PERMISSONS FOR WHO CAN USE THIS COMPUTATION
    program_id = f'{user_id}/{get_sn}'
    
    PROGRAMS = {
        "ADDITION": {
            "program_id": program_id
        }
    }
    
    with open("credential_store.json", "w") as f:
        json.dump(PROGRAMS, f, indent=4)
        
    print("PROHGRAM ID CREATED AND STORED IN THE CREDENTIAL STORE")
    
    # SETTING UP PROGRAM_BINDINGS FOR THE SPECIFIED PROGRAM_ID
    # THE PROGRAM_BINDINGS OBJECT IS USED TO DEFINE WHICH PARTIES ARE INVOLVED IN THE COMPUTATION AND HOW THEY INTERACT WITH THE PROGRAM

    compute_bindings = nillion.ProgramBindings(program_id)
    
    # THIS LINE WILL DETERMINE WHICH PARTY WILL PROVIDE SECRET
    compute_bindings.add_input_party(GAME_MANAGER_PARTY, party_id)
    
    # THIS LINE REPRESENTS THAT THE PARTY IDENTIFIED BY party_id WILL RECEIVE THE OUTPUT OF THE COMPUTATION.
    compute_bindings.add_output_party(GAME_MANAGER_PARTY, party_id)
    
    # DEINE COMPUTATIONAL TIME SECRETS BECAUSE .compute FUNCTION HAS A BUG !! FUCK IT 
    COMPUTE_SECRETS = nillion.NadaValues({})
    
    # PAY FOR THE COMPUTATION
    receipt_compute = await get_quote_and_pay(
        manager,
        nillion.Operation.compute(program_id, COMPUTE_SECRETS),
        payments_wallet,
        payments_client,
        cluster_id,
    )

    # COMPUTE BY SHOWING THE RECEIPT OF THE PAYMENT OF THE COMPUTATION
    compute_id = await manager.compute(
        cluster_id,
        compute_bindings,
        [PLAYER_INFO["store_ids"]["SYSTEM_INFO_STORE"]],
        COMPUTE_SECRETS,
        receipt_compute,
    )
    
    # THE BELOW CODE IS RESUNDANT, WE DONT NEED IT    
    # RETURN THE COMPUTATION RESULTS
    print(f"THE COMPUTATION WAS SENT THE NETWORK -> ID: {compute_id}")
    while True:
        compute_event = await manager.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"🖥️  THE UNIFIED SYSTEM IDENTIFIER FOR HARDWARE BAN {compute_event.result.value}")
            return compute_event.result.value
    
if __name__ == "__main__":
    asyncio.run(main())