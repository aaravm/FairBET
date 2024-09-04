import asyncio
import aiohttp
import py_nillion_client as nillion
import os
import random
from flask import jsonify


from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")


# async def fetch_player_alias():
#     url = "http://localhost:5000/get-player"
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 data = await response.json()
#                 return data['player_alias']
#             else: 
                # print(f"Failed to get player alias: {response.status}")
#                 return None            
            
async def fetch_target():
    url = "http://localhost:5000/get-secret-target"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response: 
            if response.status == 200:
                data= await response.json()
                secret_target = data.get('output', 'SECRET_TARGET')
                return secret_target
            else:
                # print(f"FAILED TO RETRIVE BETS: {response.status}")
                return 1
            
async def fetch_guess():
    url = "http://localhost:5000/get-secret-guess"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response: 
            if response.status == 200:
                data= await response.json()
                secret_guess = data.get('output', 'SECRET_GUESS')
                return secret_guess
            else:
                return 1
        
def generate_secret_target(target):
    
    reds = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    blacks = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
    
    def is_odd(target):
        if target % 2 != 0:
            return 101
        else:
            return False
        
    def is_even(target):
        if target % 2 == 0:
            return 102
        else: 
            return False
        
    def is_1st_12(target):
        if 0 < target <= 12:
            return 103
        else:
            return False
        
    def is_2nd_12(target):
        if 12 < target <= 24:
            return 104
        else:
            return False

    def is_3rd_12(target):
        if 24 < target <= 36:
            return 105
        else:
            return False

    def is_low(target):
        if 0 < target <= 18:
            return 106
        else:
            return False
        
    def is_high(target):
        if 18 < target <= 36:
            return 107
        else: 
            return False
    
    def is_red(target):
        if target in reds:
            return 108
        else:
            return False

    def is_black(target):
        if target in blacks:
            return 109
        else:
            return False

    def is_column_1(target):
        if target % 3 == 1:
            return 110
        else:
            return False
    
    def is_column_2(target):
        if target % 3 == 2:
            return 111
        else:
            return False
        
    def is_column_3(target):
        if target % 3 == 0 and target != 0:
            return 112
        else:
            return False
            
    
    secret_data = {
        "ODD_101": is_odd(target),                   
        "EVEN_102": is_even(target),                  
        "1ST_12_103": is_1st_12(target),             
        "2ND_12_104": is_2nd_12(target),             
        "3RD_12_105": is_3rd_12(target),              
        "LOW_106": is_low(target),                   
        "HIGH_107": is_high(target),                  
        "RED_108": is_red(target),                   
        "BLACK_109": is_black(target),               
        "COLUMN_1_110": is_column_1(target),        
        "COLUMN_2_112": is_column_2(target),        
        "COLUMN_3_113": is_column_3(target)         
    }
    
    return [value for key, value in secret_data.items() if value is not False]


async def main(): 
    
    # PLAYER_ALIAS = await fetch_player_alias()
        
    # SECRET_GUESSES = await fetch_guess()
    # print(  SECRET_GUESSES)
    PLAYER_ALIAS = "PLAYER"
    
    # random_number = random.randint(0,36)
    target = await fetch_target()
    SECRET_GUESS = await fetch_guess()
    print(f"TARGET: {target}")
    print(f"GUESS: {SECRET_GUESS}")

    SECRET_TARGETS = generate_secret_target(target)
    # SECRET_GUESS = 106

    

    if SECRET_GUESS == "3rd 12":
        SECRET_GUESS = 105
    if SECRET_GUESS == "2nd 12":
        SECRET_GUESS = 104
    if SECRET_GUESS == "1st 12":
        SECRET_GUESS = 103
    if SECRET_GUESS == "Even":
        SECRET_GUESS = 102
    if SECRET_GUESS == "Odd":
        SECRET_GUESS = 101
    if SECRET_GUESS == "1 to 18":
        SECRET_GUESS = 106
    if SECRET_GUESS == "19 to 36":
        SECRET_GUESS = 107
    if SECRET_GUESS == "Red":
        SECRET_GUESS = 108
    if SECRET_GUESS == "Black":
        SECRET_GUESS = 109
    
    # FIXMEss

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
    
    # DEPLOY THE SECRET_GUESS BY THE PLAYER

    player_secrets = nillion.NadaValues(
        {"SECRET_GUESS": nillion.SecretInteger(SECRET_GUESS)}
    )
    
    manager_secrets = nillion.NadaValues(
        {f"SECRET_TARGETS_{i}": nillion.SecretInteger(SECRET_TARGETS[i]) for i in range(len(SECRET_TARGETS))}
    )
        
    permissions = nillion.Permissions.default_for_user(player_user_id)    
    permissions.add_compute_permissions({PLAYER_CLIENT.user_id: {PROGRAM_ID}})
    permissions.add_compute_permissions({MANAGER_CLIENT.user_id: {PROGRAM_ID}})
    
    receipt_store = await get_quote_and_pay(
        PLAYER_CLIENT,
        nillion.Operation.store_values(player_secrets, ttl_days=5),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    guess_store_id = await PLAYER_CLIENT.store_values(
        cluster_id, player_secrets, permissions, receipt_store
    )
    
    permissions = nillion.Permissions.default_for_user(manager_user_id)    
    permissions.add_compute_permissions({PLAYER_CLIENT.user_id: {PROGRAM_ID}})
    permissions.add_compute_permissions({MANAGER_CLIENT.user_id: {PROGRAM_ID}})
    
    receipt_store = await get_quote_and_pay(
        MANAGER_CLIENT,
        nillion.Operation.store_values(manager_secrets, ttl_days=5),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    target_store_id = await MANAGER_CLIENT.store_values(
        cluster_id, manager_secrets, permissions, receipt_store
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

    # print(f"BLIND COMPUTATION COMPLETE: {compute_id}")

    # RETURN THE COMPUTATION RESULTS
    # print(f"THE COMPUTATION WAS SENT TO THE NETWORK -> ID: {compute_id}")
    while True:
        compute_event = await MANAGER_CLIENT.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(compute_event.result.value)
            return compute_event.result.value    
    
if __name__ == "__main__":
    asyncio.run(main())
