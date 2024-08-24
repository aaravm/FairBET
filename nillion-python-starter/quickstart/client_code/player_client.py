import asyncio
import py_nillion_client as nillion
import os

import psutil
import platform 
import subprocess
import hashlib

from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from nillion_python_helpers import create_nillion_client, create_payments_config

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
            command = "sudo dmidecode -t baseboard | grep Serial"
            serial_number = subprocess.check_output(command, shell=True).decode().split(':')[1].strip()
            system_info['serial_number'] = serial_number
        elif platform.system() == "Darwin":
            command = "system_profiler SPHardwareDataType | grep 'Serial Number (system)'"
            serial_number = subprocess.check_output(command, shell=True).decode().split(':')[1].strip()
            system_info['serial_number'] = serial_number
            
    
    except Exception as e:
        system_info['error_serial'] = str(e)
        
    return system_info

async def main():
    
    # GET NILLION-DEVNET CREDENTIALS
    cluster_id = os.getenv("NILLION_CLUSTER_ID")
    grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
    chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")
    
    seed = "PLAYER"
    user_key = UserKey.from_seed(seed)
    node_key = NodeKey.from_seed(seed)
    
    player = create_nillion_client(user_key, node_key)
    
    # REDUNDANT CODE: WE ONLY NEED THESE THINGS WHILE INTERACTING WITH THE NETWORK 
    party_id = player.party_id
    user_id = player.user_id    
    
    
    # CREATE THE PAYMENTS CONFIG, SET UP NILLION WALLET etc.
    payments_config = create_payments_config(chain_id, grpc_endpoint)
    payments_client = LedgerClient(payments_config)
    payments_wallet = LocalWallet(
        PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
        prefix="nillion",
    )
    
    
    # GET ALL THE NECESSARY USER CREDENTIALS WHICH CAN BE USED FOR HARWARE BAN: SERIAL NUMBER, PUBLIC KEY 
    # GET THE NECESSARY SYSTEM IDENTIFIERS
    system_info = get_system_info()
    serial_number = system_info['serial_number']
    
    # FIXME: MY SIZE IS TOO LARGE, I CANNOT ADJUST IN NILLION SECRETS
    wallet_addr_int = string_to_int(payments_wallet.address())
    sn_int = string_to_int(serial_number)
    
    
    
    # MOST IMPORT THING IN THE WHOLE CLIENT CODE
    with open(".env.manager", "w") as f:
        f.write(f"PLAYER_SERIAL_NUMBER={sn_int}\n")
        f.write(f"PLAYER_WALLET_ADDRESS={wallet_addr_int}")
    
    
if __name__ == "__main__":
    asyncio.run(main())