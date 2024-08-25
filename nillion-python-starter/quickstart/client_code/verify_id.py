import sys
import os
import asyncio
import requests

# Add the directory containing execute_script.py to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from execute_script import get_result_value

async def main():
    result = await get_result_value()
    print(f"Retrieved Result Value: {result}")

    url = "https://api.signprotocol.com/v1/scan/attestations/"
    # Set the query parameters
    params = {
        "schemaId": "onchain_evm_80001_0x1"
    }

    # Send the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print("Success:", data["success"])
        print("Total Attestations:", data["data"]["total"])
        print("Rows:", data["data"]["rows"])
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
    


    return True
    
if __name__ == "__main__":
    asyncio.run(main())