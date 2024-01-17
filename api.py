from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['solana_data']
collection = db['blockchain_data']
api_file = "api_data.txt"


@app.route('/lastBlock', methods=['GET'])
def last_block():
    try:
        with open(api_file, "r") as file:
            data = file.read().split('\n')
            return jsonify({"last_processed_block": int(data[0])})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/restarts', methods=['GET'])
def restart_count():
    try:
        with open(api_file, "r") as file:
            data = file.read().split('\n')
            return jsonify({"restarts": int(data[1])})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/block/<blocknum>', methods=['GET'])
def block(blocknum):
    result=collection.find_one({block: blocknum})
    blocks=list(result)
    return jsonify(blocks)
    

if __name__ == '__main__':
    app.run(host='localhost', port=8081, debug=True)
