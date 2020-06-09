from sys import stdout, path
path.append("..")

from config.config_file import baseDir
import csv
import time
from datetime import datetime
from jsonrpcclient.clients.http_client import HTTPClient

def scrapePageOfBlocks(client, height):
    response = client.send('{"jsonrpc":"2.0","id":"test","method":"f_blocks_list_json","params":{"height":%d}}' % height)
    return list(map(lambda b: {
        "Height": b["height"],
        "Hash": b["hash"],
        "Date": datetime.fromtimestamp(b["timestamp"]),
        "Difficulty": b["difficulty"],
        "Transactions": b["tx_count"],
    }, response.data.result["blocks"]))

def scrapeBlocks():
    client = HTTPClient("http://node2.ticketszones.com:27093/json_rpc")
    blocks = []
    height = 512582
    p = 1

    while height > 0:
        blocks += scrapePageOfBlocks(client, height)

        if p == 1:
            print(blocks[0])
        stdout.write("\rscraped page %d" % p)
        stdout.flush()

        if p % 50 == 0:
            with open(baseDir + "/Data/OtherChains/tickets/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 50:
                    # if this is the first 50 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/tickets/blocks.txt", "a") as logfile:
                logfile.write("scraped page %d\n (height = %d" % (p,height))

            blocks = []

        p += 1
        height -= 31
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/tickets/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/tickets/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)

def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()
