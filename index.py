import os
import requests
from pymongo import MongoClient

url = 'https://solana-mainnet.g.alchemy.com/v2/CGiyOMQ5iorRtcPm2xnU7qOSkocN2Ps7'
headers = {'Content-Type': 'application/json'}

# Connect to MongoDB 
client = MongoClient('localhost', 27017)
db = client['solana_data']
collection = db['blockchain_data']

initial_slot_file = "slot_number.txt"


if os.path.exists(initial_slot_file):
    with open(initial_slot_file, "r") as file:
        slot_number = int(file.read())
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
    with open(initial_slot_file, "w") as file:
        file.write(str(slot_number))

    client.close()
