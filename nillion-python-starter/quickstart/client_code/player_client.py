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

# FIXME: GET THIS FUNCTION IN A UTILS FILE 
def string_to_int(s):
    hash_object = hashlib.sha256(s.encode())    # USE SHA256 HASH FUNCTION
    hex_dig = hash_object.hexdigest()           # GET HEXADECIMAL DIGEST
    return int(hex_dig,  16)                    # CONVERT HEX TO INTEGER 
    
def get_system_info():
    """
    Retrives system inforamtion including processor, RAM, OS, and python version.
    Returns a dictionary with the collected data.
    """
    
    # GET GENERAL SYSTEM INFORAMATION
    system_info = {
        "processor": platform.processor(),
        "ram": f"{round(psutil.virtual_memory().total / (1024.0 ** 3))} GB",
        "os": platform.platform(),
        "python_version": platform.python_version()
    }
    
    try: 
        # FETCH MAC ADDRESS
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 8)][::-1])
        system_info['mac_address'] = mac_address
        
        # SYSTEM UUID FETCHING BASED ON OS
        if platform.system() == "Windows":
            cmd = 'wmic csproduct get uuid'
            uuid = subprocess.check_output(cmd).decode().split('\n')[1].strip()
        elif platform.system() == "Linux":
            cmd = 'dmidecode -s system-uuid'
            uuid = subprocess.check_output(cmd, shell=True).decode().strip()
        elif platform.system() == "Darwin":
            cmd = 'system_profiler SPHardwareDataType'
            output = subprocess.check_output(cmd, shell=True).decode()
            uuid_line = next(line for line in output.split('\n') if 'UUID' in line)
            uuid = uuid_line.split(': ')[1].strip()
        else:
            uuid = "UUID not available for this OS"
            
        system_info['uuid'] = uuid
        print("UUID: {}", uuid)
        
    except Exception as e: 
        system_info['error_uuid'] = str(e)
        
    try:
        # FETCH MOTHERBOARD SERIAL NUMBER
        
        if platform.system() == "Linux":
            # command = "sudo dmidecode -t baseboard | grep Serial"
            # serial_number = subprocess.check_output(command, shell=True).decode().split(':')[1].strip()
            serial_number = "Li"
            system_info['serial_number'] = serial_number
        elif platform.system() == "Darwin":
            # command = "system_profiler SPHardwareDataType | grep 'Serial Number (system)'"
            # serial_number = subprocess.check_output(command, shell=True).decode().split(':')[1].strip()
            serial_number = "Darw"
            system_info['serial_number'] = serial_number
            
    
    except Exception as e:
        system_info['error_serial'] = str(e)
        
    return system_info


def load_creds(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {"PLAYERS":{}}


def save_creds(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        

def load_player_creds(file_path, user_id, party_id, party_name): 
    credentials = load_creds(file_path)
    player_data = {
        "user_id": user_id,
        "party_id": party_id,
        "party_name": party_name
    }
    
    credentials["PLAYERS"][party_name] = player_data
    save_creds(file_path, credentials)
    

async def main():
    
    # FIXME: TO BE EXTRACTED FROM THE FRONTEND
    PLAYER_ALIAS = "PLAYER"
    
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
    
    # PUSH THE PLAYER CREDENTIALS IN THE CREDENTIAL STORE
    load_player_creds("credential_store.json", user_id, party_id, PLAYER_ALIAS)
    
    # CREATE THE PAYMENTS CONFIG, SET UP NILLION WALLET etc.
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )
    
    # DEPLOY THE PROGRAM 
    PROGRAM_NAME = "addition"
    PROGRAM_PATH = f"../nada_quickstart_programs/target/{PROGRAM_NAME}.nada.bin"
    
    receipt_store_program = await get_quote_and_pay(
        player,
        nillion.Operation.store_program(PROGRAM_PATH),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    action_id = await player.store_program(
        cluster_id, PROGRAM_NAME, PROGRAM_PATH, receipt_store_program
    )
    
    PROGRAM_ID = f'{user_id}/{PROGRAM_NAME}'
    
    # GET ALL THE NECESSARY USER CREDENTIALS WHICH CAN BE USED FOR HARWARE BAN: SERIAL NUMBER, PUBLIC KEY 
    # GET THE NECESSARY SYSTEM IDENTIFIERS
    system_info = get_system_info()
    serial_number = system_info['serial_number']
    
    print(f"SERIAL NUMBER: {serial_number}")
    print(f"WALLET ADDRESS: {payments_wallet.address()}")
    
    # FIXME: MY SIZE IS TOO LARGE, I CANNOT ADJUST IN NILLION SECRETS
    wallet_addr_int = string_to_int(payments_wallet.address())
    sn_int = string_to_int(serial_number)
    
    NEW_SECRETS = nillion.NadaValues(
        {
            "SECRET1": nillion.SecretInteger(sn_int),
            "SECRET2": nillion.SecretInteger(wallet_addr_int)        # FIXME: REPLACE THIS 20 WITH WALLET_ADDR_INT
        }
    )
    
    permissions = nillion.Permissions.default_for_user(player.user_id)    
    permissions.add_compute_permissions({player.user_id: {PROGRAM_ID}})
    
    receipt_store = await get_quote_and_pay(
        player,
        nillion.Operation.store_values(NEW_SECRETS, ttl_days=5),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    store_id = await player.store_values(
        cluster_id, NEW_SECRETS, permissions, receipt_store
    )
    
    print(f"SERIAL NUMBER AND WALLET ADDRESS STORED: {store_id}")
    
    # SET UP COMPUTATION OF THE SECRETS
    
    compute_bindings = nillion.ProgramBindings(PROGRAM_ID)
    compute_bindings.add_input_party(PLAYER_ALIAS, party_id)
    compute_bindings.add_output_party(PLAYER_ALIAS, party_id)
    
    COMPUTE_SECRETS = nillion.NadaValues({})
    
    receipt_compute = await get_quote_and_pay(
        player,
        nillion.Operation.compute(PROGRAM_ID, COMPUTE_SECRETS),
        payments_wallet,
        payments_client,
        cluster_id
    )
    
    compute_id = await player.compute(
        cluster_id,
        compute_bindings,
        [store_id],
        COMPUTE_SECRETS,
        receipt_compute
    )
    
    print(f"BLIND COMPUTATION COMPLETE: {compute_id}")
    
    # THE BELOW CODE IS RESUNDANT, WE DONT NEED IT    
    # RETURN THE COMPUTATION RESULTS
    print(f"THE COMPUTATION WAS SENT THE NETWORK -> ID: {compute_id}")
    while True:
        compute_event = await player.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            print(f"🖥️  THE UNIFIED SYSTEM IDENTIFIER FOR HARDWARE BAN {compute_event.result.value}")
            return compute_event.result.value
    
    
if __name__ == "__main__":
    asyncio.run(main())