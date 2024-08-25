import sys
import os
import asyncio
import requests
from eth_abi import decode
import re

# Add the directory containing execute_script.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from execute_script import get_result_value

async def main():
    result = await get_result_value()
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