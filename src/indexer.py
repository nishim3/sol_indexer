import os
import json
from pymongo import MongoClient
from websocket import create_connection
import ssl
import time

url = 'wss://solana-mainnet.g.alchemy.com/v2/CGiyOMQ5iorRtcPm2xnU7qOSkocN2Ps7'
headers = {'Content-Type': 'application/json'}

# Connect to MongoDB
client = MongoClient('localhost', 27017)
db = client['solana_data']
collection = db['blockchain_data']
logs = "logs.txt"

slot_number = 0
restart_count = 0
if not os.path.exists(logs):
    with open(logs, "w") as file:
        slot_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSlot"
        }
        ws = create_connection(url, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.send(json.dumps(slot_data))
        response = ws.recv()
        slot_number = json.loads(response)['result']
        ws.close()
else:
    with open(logs, "r") as file:
        data = file.read().split('\n')
        slot_number = int(data[0])
        restart_count = int(data[1])

last_processed_block = 0
islot = slot_number
itime = None
processing_time = None
avg_speed = None

try:
    while True:
        print(f"Indexing block: {slot_number}")
        # Fetch the block for the current slot
        itime = time.time()
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

        ws = create_connection(url, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.send(json.dumps(block_data))
        response = ws.recv()
        response_json = json.loads(response)
        ws.close()

        for transaction in response_json['result']['transactions']:
            transaction['block'] = slot_number
            collection.insert_one(transaction)

        last_processed_block = slot_number
        processing_time = time.time() - itime
        avg_speed = (last_processed_block - islot) / (time.time() - itime)
        slot_number += 1
        with open(logs, "w") as file:
            file.write(f"{last_processed_block}\n{restart_count}\n{processing_time}\n{avg_speed}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Increment restart count
    restart_count += 1

    # Update api file with slot number and restart count
    with open(logs, "w") as file:
        file.write(f"{last_processed_block}\n{restart_count}\n{processing_time}\n{avg_speed}")

    client.close()
