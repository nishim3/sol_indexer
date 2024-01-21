Solana Blockchain Data Indexer and API
This project consists of two main components: a Solana blockchain data indexer and a Flask API. The indexer fetches Solana blockchain data from a specified API endpoint and stores it in a MongoDB database. The Flask API provides endpoints to retrieve information about the processed blockchain data.

Indexer
Prerequisites
Python 3.x
Required Python packages (install using pip install -r requirements.txt):
requests
pymongo
Usage
Ensure that MongoDB is installed and running locally on the default port (27017).

Update the url variable in the indexer.py file with the Solana API endpoint.

Run the indexer.py script:

bash
Copy code
python indexer.py
The script will continuously fetch Solana blockchain data and store it in the MongoDB collection named blockchain_data.

Flask API
Prerequisites
Python 3.x
Required Python packages (install using pip install -r requirements.txt):
Flask
pymongo
bson
Usage
Ensure that MongoDB is installed and running locally on the default port (27017).

Update the logs variable in the api.py file with the path to the logs file.

Run the api.py script:

bash
Copy code
python api.py
The Flask API will start running on http://localhost:8081/.

API Endpoints
/lastBlock: Get the last processed block number.
/restarts: Get the restart count of the indexer.
/ispeed: Get information about the last processed block and the time taken.
/avgblockspeed: Get the average block processing speed.
/transactioncount/<blocknum>: Get the number of transactions in a specific block.
/transactions/<blocknum>: Get a list of transactions in a specific block.
Contributing
Feel free to contribute to this project by opening issues or submitting pull requests.

License
This project is licensed under the MIT License - see the LICENSE file for details.

