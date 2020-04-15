from sys import stdout, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
import csv
import time
from datetime import datetime

def scrapePageOfBlocks(p, headers):
    url = "https://explorer-backend.nebulas.io/api/blocks?p=%d" % p
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    response = json.load(response)

    blocks = response["data"]["data"]
    return list(map(lambda b: {
        "Height": b["height"],
        "Hash": b["hash"],
        "Date": datetime.fromtimestamp(b["timestamp"] / 1000),
        "Gas limit": b["gasLimit"],
        "Gas reward": b["gasReward"],
        "Average gas price": b["avgGasPrice"],
        "Miner id": b["miner"]["id"],
        "Miner hash": b["miner"]["hash"]
    }, blocks))

def scrapeBlocks():
    blocks = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }

    for p in range(45801,160338):
        blocks += scrapePageOfBlocks(p, headers)

        if p == 1:
            print(blocks[0])
        stdout.write("\rscraped page %d" % p)
        stdout.flush()

        if p % 100 == 0:
            with open(baseDir + "/Data/OtherChains/nebulas/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 100:
                    # if this is the first 1000 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/nebulas/blocks.txt", "a") as logfile:
                logfile.write("scraped page %d\n" % p)

            blocks = []
        p -= 1
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/nebulas/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/nebulas/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()