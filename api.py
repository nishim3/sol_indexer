from flask import Flask, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
import json
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['solana_data']
collection = db['blockchain_data']
logs = "logs.txt"



@app.route('/lastBlock', methods=['GET'])
def last_block():
    try:
        with open(logs, "r") as file:
            data = file.read().split('\n')
            return jsonify({"last_processed_block": int(data[0])})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/restarts', methods=['GET'])
def restart_count():
    try:
        with open(logs, "r") as file:
            data = file.read().split('\n')
            return jsonify({"restarts": int(data[1])})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/ispeed', methods=['GET'])
def ispeed():
    with open(logs, "r") as file:
        data = file.read().split('\n')
        return jsonify({
            "last_processed_block": int(data[0]),
            "time" : data[2]
        })

@app.route('/avgblockspeed', methods=['GET'])
def avgbs():
    try:
        with open(logs, "r") as file:
            data = file.read().split('\n')
            return jsonify({
                "Average speed ": f"{data[3]} blocks/s"
            })
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/transactioncount/<blocknum>', methods=['GET'])
def no_of_transactions(blocknum):
    result=collection.count_documents({'block': int(blocknum)})
    return jsonify({
        "block": f"{blocknum}",
        "transactions": f"{result}"
    })

@app.route('/transactions/<blocknum>', methods=["GET"])
def block(blocknum):
    result=collection.find({'block': int(blocknum)})
    block_list = [transact.get('transaction') for transact in result]
    return jsonify(block_list)



if __name__ == '__main__':
    app.run(host='localhost', port=8081, debug=True)
