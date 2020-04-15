from sys import stdout, path
path.append("..")

from config.config_file import baseDir
import csv
import time
from datetime import datetime
from jsonrpcclient.clients.http_client import HTTPClient

def scrapePageOfBlocks(client, start, end):
    response = client.send('{"jsonrpc":"2.0","method":"getblocks","params":[%d,%d],"id":1}' % (start,end))

    return list(map(lambda b: {
        "Height": b["index"],
        "Hash": b["hash"],
        "Date": datetime.fromtimestamp(b["time"]),
        "Version": b["version"],
        "Validator": b["validator"],
        "Transactions": b["transactions"],
        "Total net fee": float(b["total_net_fee"]),
        "Total sys fee": float(b["total_sys_fee"])
    }, response.data.result))

def scrapeBlocks():
    client = HTTPClient("https://explorer.o3node.org/")
    blocks = []
    start = 3282094 
    end = 3283093
    p = 1851
    
    while start > 0:
        blocks += scrapePageOfBlocks(client, start, end)

        if p == 1:
            print(blocks[0])
        stdout.write("\rscraped page %d" % p)
        stdout.flush()

        if p % 50 == 0:
            with open(baseDir + "/Data/OtherChains/neo/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 50:
                    # if this is the first 50 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/neo/blocks.txt", "a") as logfile:
                logfile.write("scraped page %d\n ([start end] = [%d %d]" % (p,start,end))

            blocks = []
        p += 1
        start -= 1000
        end -= 1000
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/neo/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/neo/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()


