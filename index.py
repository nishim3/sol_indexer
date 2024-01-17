import os
import requests
from pymongo import MongoClient

url = 'https://solana-mainnet.g.alchemy.com/v2/CGiyOMQ5iorRtcPm2xnU7qOSkocN2Ps7'
headers = {'Content-Type': 'application/json'}

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['solana_data']
collection = db['blockchain_data']

api_file = "api_data.txt"

# Initialize slot number and restart count
slot_number = 0
restart_count = 0

# Check if the api file exists
if os.path.exists(api_file):
    with open(api_file, "r") as file:
        data = file.read().split(',')
        if len(data) == 2:
            slot_number, restart_count = map(int, data)
else:
    slot_data = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getSlot"}

    slot_response = requests.post(url, json=slot_data, headers=headers)
    slot_number = slot_response.json()['result']


try:
    while True:
        print(f"Indexing block: {slot_number}")

        # Fetch the block for the current slot
        block_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlock",
            "params": [
                slot_number,
                {
                    "encoding": "json",
                    "maxSupportedTransactionVersion": 0,
                    "transactionDetails": "full",
                    "rewards": False
                }
            ]
        }

        response = requests.post(url, json=block_data, headers=headers)
        response_json = response.json()

        for transaction in response_json['result']['transactions']:
            transaction['block'] = slot_number
            collection.insert_one(transaction)

        slot_number += 1

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Increment restart count
    restart_count += 1

    # Update api file with slot number and restart count
    with open(api_file, "w") as file:
        file.write(f"{slot_number},{restart_count}")

    client.close()
