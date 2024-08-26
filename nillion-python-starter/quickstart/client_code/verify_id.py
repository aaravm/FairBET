import sys
import os
import asyncio
import requests
from eth_abi import decode
import re
import subprocess
import asyncio

# Add the directory containing execute_script.py to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# from execute_script import get_result_value

async def get_result_value():
    try:
    # Run player_client.py
        current_dir = os.getcwd()
        target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))

        # Determine the command to run based on the current directory
        if current_dir != target_dir:
            command = f"cd {target_dir} && python3 player_client.py"
        else:
            command = "python3 player_client.py"

        # Run the command
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        
        # Extract the value of compute_event.result.value from the output
        for line in result.stdout.split('\n'):
            if "🖥️  THE UNIFIED SYSTEM IDENTIFIER FOR HARDWARE BAN" in line:
                value = line.split()[-1]
                if value.endswith('}'):
                    value = value[:-1]
                return value
        
        # If value doesn't get returned, use this defaultr instead
        result_value= "Jinesh123"
        return result_value
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit status {e.returncode}")
        print(f"Error output: {e.stderr}")
        return "Jinesh123"


async def main():
    result = await get_result_value()
    # result = "Jinesh12efhaoweo3"
    print(f"Retrieved Result Value: {result}")

    url = "https://testnet-rpc.sign.global/api/index/attestations/"
    # Set the query parameters
    params = {
        "schemaId": "onchain_evm_84532_0xd1"
    }

    # Send the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print("Success:", data["success"])
        print("Total Attestations:", data["data"]["total"])
        for i in data["data"]["rows"]:
            clean_hex = re.sub(r'^0x', '', i["data"])  # Remove "0x" prefix if present
            decoded_data = decode(['string'], bytes.fromhex(clean_hex))
            if result == decoded_data[0]:
                return False

    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
    return True

if __name__ == "__main__":
    result = asyncio.run(main())
    print(f"Main function returned: {result}")