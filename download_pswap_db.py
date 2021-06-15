import sqlite3
import requests
import os.path
from pprint import pprint


####SETUP####

# 1) Write the path you want to save the DB here:

PATH = "D:/Francesco/Desktop/Defi Project/Download DB/DBs pswap/"

# 2) Write the address of the account you want to download the transactions of:

ADDRESS = "0xEa26B78255Df2bBC31C1eBf60010D78670185bD0"


def create_connection(dbName):
    conn = None
    try:
        conn = sqlite3.connect(PATH + dbName)
        return conn
    except sqlite3.Error as e:
        print(e)

def create_table(conn, name):
   
    statement = """ CREATE TABLE IF NOT EXISTS {}(
                                        blockHash TEXT,
                                        blockNumber BIGINT,
                                        confirmations BIGINT ,
                                        contractAddress TEXT ,
                                        cumulativeGasUsed BIGINT,
                                        fromAddr TEXT,
                                        gas BIGINT , 
                                        gasPrice BIGINT,
                                        hash TEXT,
                                        input TEXT, 
                                        nonce BIGINT, 
                                        timeStamp TEXT,
                                        toAddr TEXT,
                                        tokenDecimal BIGINT,
                                        tokenName TEXT,
                                        tokenSymbol TEXT,
                                        transactionIndex BIGINT,
                                        value BIGINT 
                                        ); """.format(name)

    
    try:
        c = conn.cursor()
        c.execute(statement)
    except sqlite3.Error as e:
        print(e)

def insert_in_transactions(conn, transaction):

    #transaction_tuple = (transaction[0],"??", transaction[11],transaction[1], transaction[2],transaction[3], transaction[4], transaction[5], transaction[6],transaction[7], transaction[8],transaction[9], transaction[10], transaction[12], transaction[13],transaction[14], transaction[15],transaction[16], transaction[17])

    transaction_tuple= (
                        transaction["blockHash"], 
                        transaction["blockNumber"],
                        transaction["confirmations"],
                        transaction["contractAddress"],
                        transaction["cumulativeGasUsed"],
                        transaction["from"],
                        transaction["gas"],
                        transaction["gasPrice"],
                        transaction["hash"],
                        transaction["input"],
                        transaction["nonce"],
                        transaction["timeStamp"],
                        transaction["to"],
                        transaction["tokenDecimal"],
                        transaction["tokenName"],
                        transaction["tokenSymbol"],
                        transaction["transactionIndex"],
                        int(transaction["value"]) / (10**int(transaction["tokenDecimal"]))
                        )
     

    c = conn.cursor()
    statement = """INSERT INTO transactions
                                (blockHash,
                                blockNumber, 
                                confirmations, 
                                contractAddress, 
                                cumulativeGasUsed, 
                                fromAddr,
                                gas, 
                                gasPrice, 
                                hash,
                                input, 
                                nonce, 
                                timeStamp,
                                toAddr, 
                                tokenDecimal, 
                                tokenName, 
                                tokenSymbol, 
                                transactionIndex, 
                                value) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """

#     sql = """INSERT INTO transactions (blockHash, toAddr) VALUES (?,?)"""
    c.execute(statement, transaction_tuple)

 #   pprint("DONE: " + transaction["blockNumber"])

    conn.commit()

def delete_all(conn):
    statement = "DELETE FROM transactions"

    cur = conn.cursor()
    cur.execute(statement)

    conn.commit()   

def get_all(conn):
    statement = "SELECT * FROM transactions"

    cur = conn.cursor()
    cur.execute(statement)

    rows = cur.fetchall()

    return len(rows)

def get_last_blockNumber(conn):
    statement = "SELECT MAX(blockNumber) from transactions;"

    cur = conn.cursor()
    cur.execute(statement)

    rows = cur.fetchall()

    return rows[0][0]

def delete_block(conn, blockNumber):

    pprint("Starting to download from block: " + str(blockNumber))

    statement = "DELETE from transactions WHERE blockNumber == {}".format(blockNumber)

    cur = conn.cursor()
    cur.execute(statement)

    conn.commit()


if __name__ == '__main__':
    alreadyExist = False
    address = ADDRESS
    dbName = "DB-" + address
    if os.path.exists(PATH + dbName):
        alreadyExist = True
    conn = create_connection(dbName)
    startBlock = 0
    endBlock = 99999999
    flag = 0
    numberOfTransactions = 0

    with conn: 
        
        
        pprint('Creating Database of contract: ' + address)
        pprint('DB NAME: ' + dbName)

        if alreadyExist == True:
            pprint("This DB already exists...")
            _input = input("Do you want to UPDATE or RESET your DB? (type R to reset, anything to UPDATE) ")
            while(alreadyExist):
                if(_input == "R"):
                    _input = input("Are you sure? ")

                    if(_input == "y" or _input == ""):
                        delete_all(conn)
                        alreadyExist = False
                else:
                    last_block = get_last_blockNumber(conn)
                    delete_block(conn, last_block)
                    startBlock = last_block
                    alreadyExist = False
        else:
            create_table(conn, "transactions")
        
        _input = input("Get all blocks? ")
        if(_input == "y" or _input == ""):
            endBlock = 9999999
        else:
            endBlock = input("Write the FINAL BLOCK: ")
#        endBlock = input("Write the historical date: ") TO_DO!

        p = pprint("Downloading from etherscan")

        while(flag != 1):
        #    for i in range(0,5):     
            
            etherscan_request = requests.get('https://api.bscscan.com/api?module=account&action=tokentx&address={}&startblock={}&endblock={}&sort=asc&apikey=K98IZN13XTQKJGAX8IXP6EBGQ9FDJKQJ8B'.format(address,startBlock, endBlock))
            json_data = etherscan_request.json()["result"]

            l = len(json_data)
            pprint("BlockNumber -> " + str(startBlock))
            pprint("Transaction analyzed -> " + str(numberOfTransactions))
            if(l == 0):
                pprint("No transaction to analyze!")
                break
            numberOfTransactions += l
            pprint("Inserting " + str(l) + " transactions in DB")

            last_block = int(json_data[-1]["blockNumber"])

            for transasction in json_data:
#               pprint(transasction)
                if(int(transasction["blockNumber"]) != last_block or l < 10000):
                    insert_in_transactions(conn,transasction)

            startBlock = last_block

            if(l < 10000):
                pprint("Download completed!")
                pprint("Last transactions block: " + str(last_block))
                flag = 1
                break

       #     time.sleep(1)

        
        rows = get_all(conn)
        pprint("Number of transactions analyzed: " + str(numberOfTransactions))
        pprint("DB length: " + str(rows))
