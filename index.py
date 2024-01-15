import requests
from pymongo import MongoClient

url = 'https://solana-mainnet.g.alchemy.com/v2/CGiyOMQ5iorRtcPm2xnU7qOSkocN2Ps7'
headers = {'Content-Type': 'application/json'}

# Connect to MongoDB (make sure MongoDB is running on your machine)
client = MongoClient('localhost', 27017)
db = client['solana_data']
collection = db['blockchain_data']
slot_data = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getSlot"
}

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

        # Add 'block' parameter to each transaction
        for transaction in response_json['result']['transactions']:
            transaction['block'] = slot_number

            # Insert each transaction into the MongoDB collection
            collection.insert_one(transaction)

        slot_number += 1

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Sort transactions in descending order of 'block' before closing the MongoDB connection
    sorted_transactions = collection.find().sort("block", -1)
   

    # Close the MongoDB connection (this line is reached if an exception occurs or the loop exits)
    client.close()
