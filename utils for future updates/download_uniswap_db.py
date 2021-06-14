from sqlite3.dbapi2 import Timestamp
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from matplotlib import pyplot as plt
from numpy.lib import type_check
from pwnlib.replacements import sleep
import requests
import sqlite3

from pprint import pprint


def create_connection(dbName):
    conn = None
    try:
        conn = sqlite3.connect("D:/Francesco/Desktop/Defi Project/web3js/" + dbName)
        return conn
    except sqlite3.Error as e:
        print(e)

def create_table(conn, name):
   
    statement = """ CREATE TABLE IF NOT EXISTS {}(
                                        blockNumber BIGINT,
                                        timeStamp TEXT,
                                        liquidityUSD BIGINT,
                                        volumeUSD BIGINT
                                        ); """.format(name)

    
    try:
        c = conn.cursor()
        c.execute(statement)
    except sqlite3.Error as e:
        print(e)

def insert_line(conn, tuple):

    #transaction_tuple = (transaction[0],"??", transaction[11],transaction[1], transaction[2],transaction[3], transaction[4], transaction[5], transaction[6],transaction[7], transaction[8],transaction[9], transaction[10], transaction[12], transaction[13],transaction[14], transaction[15],transaction[16], transaction[17])


    c = conn.cursor()
    statement = """INSERT INTO uniswap
                                (blockNumber,
                                timestamp, 
                                liquidityUSD, 
                                volumeUSD
                                ) VALUES (?,?,?,?) """

#     sql = """INSERT INTO transactions (blockHash, toAddr) VALUES (?,?)"""
    c.execute(statement, tuple)

 #   pprint("DONE: " + transaction["blockNumber"])

    conn.commit()

def delete_all(conn):
    statement = "DELETE FROM uniswap"

    cur = conn.cursor()
    cur.execute(statement)

    conn.commit()   

def get_all(conn):
    statement = "SELECT * FROM uniswap"

    cur = conn.cursor()
    cur.execute(statement)

    rows = cur.fetchall()

    return rows



sample_transport=RequestsHTTPTransport(
    url='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2',
    verify=True,
    retries=5,
)
client = Client(
    transport=sample_transport
)

blocks = []
liquidity = []
volumes = []

block = 12606044

while block > 12500000: 
    query = gql('''
    query {
  pair (id: "0x3041cbd36888becc7bbcbc0045e3b1f144466f5f", block: {number:''' + str(block) + ''' }){
    id
    token0{
      symbol
    }
    token1{
      symbol
    }
    reserveUSD
    volumeUSD
  }
}
    ''')
    response = client.execute(query)
    
    
    liquidityUSD = response['pair']['reserveUSD']
    volumeUSD = response['pair']['volumeUSD']

    blocks.insert(0, block)
    liquidity.insert(0, liquidityUSD)
    volumes.insert(0, volumeUSD)

    block = block - 1000
    print(block)

pprint(blocks)
pprint(liquidity)
pprint(volumes)

liquidity = [float(x) for x in liquidity]
volumes = [float(x) for x in volumes]

timeStamps = []

for i in range(0, len(blocks)):
    etherscan_request = requests.get('https://api.etherscan.io/api?module=block&action=getblockreward&blockno={}&apikey=MUQRF4N8I83RRSIAX76JXMEGKTBSN9PAWZ'.format(blocks[i]))
    json_data = etherscan_request.json()['result']
    if isinstance(json_data, str):
        sleep(1)
        pprint("waiting")
    else:
        timeStamps.append(json_data['timeStamp'])
        i = i+1

    

pprint(blocks)
pprint(timeStamps)

    
conn = create_connection("uniswap")



with conn:
    delete_all(conn)
    create_table(conn, "uniswap")

    for i in range(0, len(blocks)):
        tuple = (blocks[i], timeStamps[i], liquidity[i], volumes[i])

        insert_line(conn, tuple)



# normalize or standardize data as
'''
liquidity = [float(i) for i in liquidity]
volume = [float(i) for i in volume]
transactions = [float(i) for i in transactions]
liquidity = [float(i)/sum(liquidity) for i in liquidity]
volume = [float(i)/sum(volume) for i in volume]
transactions = [float(i)/sum(transactions) for i in transactions]
#title = 'Uniswap Liquidity Over Time'
labels = ['Liquidity', 'Volume', 'Transactions']
'''


