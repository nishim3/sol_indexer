
# Solana Indexer

This python application provides two APIs for retrieving performance-related data. Follow the instructions below to call these APIs.

## API Endpoints

### Last Block

- **Endpoint:** `/lastBlock`
- **Description:** Returns the last processed block.
- **HTTP Method:** GET
- **Example Request:**
  ```bash
  curl -X GET http://localhost:8081/lastBlock
  ```
- **Example Response:**
  ```bash
  {
  "last_processed_block": 243149411
  }
  ```

### Restarts

- **Endpoint:** `/restarts`
- **Description:** Retrieves the number of restarts.
- **HTTP Method:** GET
- **Path Parameter:**
  - none
- **Example Request:**
  ```bash
  curl -X GET http://localhost:8081/restarts
  ```
- **Example Response:**
  ```bash
  {
  "restarts": 2
  }
  ```

  ### Time taken to process last block

- **Endpoint:** `/ispeed`
- **Description:** Retrieves the time taken to process last block.
- **HTTP Method:** GET
- **Path Parameter:**
  - none
- **Example Request:**
  ```bash
  curl -X GET http://localhost:8081/ispeed
  ```
- **Example Response:**
  ```bash
  {
  "last_processed_block": 243149471,
  "time": "2.1563560962677"
  }
  ```
   ### Average block speed

- **Endpoint:** `/avgblockspeed`
- **Description:** Retrieves the average speed of block indexing.
- **HTTP Method:** GET
- **Path Parameter:**
  - none
- **Example Request:**
  ```bash
  curl -X GET http://localhost:8081/avgblockspeed
  ```
- **Example Response:**
  ```bash
  {
  "Average speed ": "0.25691177728441217 blocks/s"
  }
  ```
   ### Transactions per block

- **Endpoint:** `/transactioncount/<blocknum>`
- **Description:** Retrieves the number of transactions per block.
- **HTTP Method:** GET
- **Path Parameter:**
  - block number
- **Example Request:**
  ```bash
  curl -X GET http://localhost:8081/transactioncount/243149471
  ```
- **Example Response:**
  ```bash
  {
  "block": "243149471",
  "transactions": "601"
  }
  ```
   ### Transactions of a block

- **Endpoint:** `/transactions/<blocknum>`
- **Description:** Retrieves the transactions of each block.
- **HTTP Method:** GET
- **Path Parameter:**
  - block number
- **Example Request:**
  ```bash
  curl -X GET http://localhost:8081/transactions/243149471
  ```
  
## How to Use

1. Start the application by running the following commands:
   ```bash
   python api.py 
   ```
   In a separate terminal, start
    ```bash
   python indexer.py 
   ```
   
3. Once the application is running, you can make API requests using `curl` or any other HTTP client of your choice.

     ```bash
     curl -X GET http://localhost:8081/transactions/<blocknum>     ```
     Replace `<blocknum>` with the block number.

     ```

4. You will get outputs in JSON files.
5. For further querying the database, you can connect to mongodb://localhost:27017 and query using mongosh or compass.
