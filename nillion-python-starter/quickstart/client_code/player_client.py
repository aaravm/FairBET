"""
In this example, we:
1. connect to the local nillion-devnet
2. store the secret addition program
3. store a secret to be used in the computation
4. compute the secret addition program with the stored secret and another computation time secret
"""

import asyncio
import py_nillion_client as nillion
import os

import psutil
import platform 
import subprocess
import hashlib

from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

home = os.getenv("HOME")
load_dotenv(f"{home}/.config/nillion/nillion-devnet.env")

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
        command = "sudo dmidecode -t baseboard | grep Serial"
        serial_number = subprocess.check_output(command, shell=True).decode().split(':')[1].strip()
        system_info['serial_number'] = serial_number
    
    except Exception as e:
        system_info['error_serial'] = str(e)
        
    return system_info

async def main():
    
    # GET THE NECESSARY SYSTEM IDENTIFIERS
    system_info = get_system_info()
    serial_number = system_info['serial_number']
    os_id = system_info['os']
    
    sn_int = string_to_int(serial_number)
    os_int = string_to_int(os_id)
    
    # GET NILLION-DEVNET CREDENTIALS
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")


    # INITIATE A NILLION CLIENT USING THE SEED
    seed = "my_seed"
    userkey = UserKey.from_seed(seed)
    nodekey = NodeKey.from_seed(seed)

    player = create_nillion_client(userkey, nodekey)

    party_id = player.party_id
    user_id = player.user_id
    
    # HOW WILL BE STORE THE COMPUTATION PROGRAMS ??
    # WE CREATE DIFFERENT COMPUATION PROGRAMS AND REFER TO THEIR .nada.bin FILE.
    # DEPLOY ALL THE COMPUTATIONS IN DEVNET
    
    get_sn = "addition"
    get_sn_path =  f"../nada_quickstart_programs/target/{get_sn}.nada.bin"
    
    # CREATE THE PAYMENTS CONFIG, SET UP NILLION WALLET etc.
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )
    
    # PAY FOR DEPLOYMENT
    receipt_store_program = await get_quote_and_pay(
        player,
        nillion.Operation.store_program(get_sn_path),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    # STORE THE PROGRAM BY SHOWING THE RECEIPT
    action_id = await player.store_program(
        cluster_id, get_sn, get_sn_path, receipt_store_program
    )

    # NOW WE CREATE A VARIABLE FOR THE PROGRAM ID TO SET PERMISSONS FOR WHO CAN USE THIS COMPUTATION
    program_id = f"{user_id}/{get_sn}"
    print("PROGRAM STORED -> ID:", program_id)
    
    
    # SECRET INSTANCES CREATION
    NEW_SECRETS = nillion.NadaValues(
        {
            "SECRET1": nillion.SecretInteger(sn_int),
            "SECRET2": nillion.SecretInteger(os_int)
        }
    )
    
    GAME_MANAGER_PARTY = "PLAYER"
    PLAYER_PARTY = "PLAYER"
    
    # SET THE PERMISSIONS TO ALLOW THE USER TO PERFORM COMPUTATION ON THE SECRETS FOR THE SPECIIFIED PROGRAM_ID
    permissions = nillion.Permissions.default_for_user(player.user_id)
    permissions.add_compute_permissions({player.user_id: {program_id}})

    # PAY T0 DEPLOYMENT OF THE SECRET
    receipt_store = await get_quote_and_pay(
        player,
        nillion.Operation.store_values(NEW_SECRETS, ttl_days=5),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    # STORE THE SECRET BY SHOWING THE RECEIPT
    store_id = await player.store_values(
        cluster_id, NEW_SECRETS, permissions, receipt_store
    )
    print(f"SECRETS STORED -> ID: {store_id}")
    
    # SET UP PROGRAM_BINDINGS FOR THE SPECIFIED PROGRAM_ID
    # THE PROGRAM_BINDINGS OBJECT IS USED TO DEFINE WHICH PARTIES ARE INVOLVED IN THE COMPUTATION AND HOW THEY INTERACT WITH THE PROGRAM
    compute_bindings = nillion.ProgramBindings(program_id)
    
    # THIS LINE WILL DETERMINE WHICH PARTY WILL PROVIDE SECRET
    # IN CASE OF SYSTEM IDENTIFIERS, THE PLAYER
    compute_bindings.add_input_party(PLAYER_PARTY, party_id)
    
    # THIS LINE REPRESENTS THAT THE PARTY IDENTIFIED BY party_id WILL RECEIVE THE OUTPUT OF THE COMPUTATION.
    # IN CASE OF THE PLAYER'S SYSTEM IDENTIFIER, THE GAME MANAGER
    
    # TO GIVE THE OUTPUT VALUE TO THE GAME MANAGER, WE NEED TO FIRST CREATE A GAME MANAGER CLIENT AND DEPLOY IT, SO WE CAN USE ITS PARTY_ID
    compute_bindings.add_output_party(GAME_MANAGER_PARTY, party_id)

    # PAY FOR THE COMPUTATION
    receipt_compute = await get_quote_and_pay(
        player,
        nillion.Operation.compute(program_id),
        payments_wallet,
        payments_client,
        cluster_id,
    )
    
    # COMPUTE BY SHOWING THE RECEIPT OF THE PAYMENT OF THE COMPTATION
    compute_id = await player.compute(
        cluster_id,
        compute_bindings,
        [store_id],
        None,        # NO COMPUTATION TIME SECRETS 
        receipt_compute,
    )

    # RETURN THE COMPUTATION RESULTS
    print(f"THE COMPUTATION WAS SENT THE NETWORK -> ID: {compute_id}")
    while True:
        compute_event = await player.next_compute_event()
        if isinstance(compute_event, nillion.ComputeFinishedEvent):
            # print(f"✅  Compute complete for compute_id {compute_event.uuid}")
            print(f"🖥️  THE UNIFIED SYSTEM IDENTIFIER FOR HARDWARE BAN {compute_event.result.value}")
            return compute_event.result.value

    
if __name__ == "__main__":
    asyncio.run(main())