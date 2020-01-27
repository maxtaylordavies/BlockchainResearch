from six.moves import urllib
import json
from etherscan import baseDir
import csv
from sys import stdout
import time
from datetime import datetime

def scrapePageOfBlocks(p, headers):
    url = "https://blockmeta.com/api/v3/blocks?page=" + str(p) + "&limit=500"
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    data = json.load(response)
    blocks = data["blocks"]

    if not blocks:
        return []

    return list(map(lambda b: {
        "Height": b["height"],
        "Hash": b["hash"],
        "Time": datetime.fromtimestamp(b["time"]),
        "Miner": b["miner"],
        "Size": b["size"],
        "Transaction count": b["transaction_count"],
        "Difficulty": b["difficulty"],
        "Miner name": b["miner_name"],
        "Miner address": b["miner_address"],
        "Chain status": b["chain_status"],
        "Version": b["version"]
    }, blocks))

def scrapeBlocks():
    blocks = []
    p = 1
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }

    while True:
        blocks += scrapePageOfBlocks(p, headers)

        if p == 1:
            print(blocks[0])

        stdout.write("\r%d iterations" % p)
        stdout.flush()

        if p % 20 == 0:
            with open(baseDir + "/Data/OtherChains/bytom/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 20:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/bytom/blocks.txt", "a") as logfile:
                logfile.write("%d pages scraped\n" % p)

            blocks = []

        p += 1
    
    with open(baseDir + "/Data/OtherChains/bytom/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/bytom/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()