from sys import stdout, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
import csv
import time
from datetime import datetime

def scrapePageOfBlocks(p, headers):
    url = "https://vtc.tokenview.com/api/blocks/vtc/%d/1000" % p
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    response = json.load(response)

    if response["code"] == 404:
        return []

    blocks = response["data"]
    return list(map(lambda b: {
        "Network": b["network"],
        "Height": b["block_no"],
        "Date": datetime.fromtimestamp(b["time"]).strftime("%Y-%m-%d %H:%M:%S"),
        "Size": b["size"],
        "Transaction count": b["txCnt"],
        "Sent value": float(b["sentValue"]),
        "Miner address": b["miner"],
        "Fee": float(b["fee"]),
        "Reward": float(b["reward"]),
        "Difficulty": float(b["miningDifficulty"])
    }, blocks))

def scrapeBlocks():
    blocks = []
    p = 661
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }

    while True:
        newBlocks = scrapePageOfBlocks(p, headers)
        if not newBlocks:
            break
        blocks += newBlocks

        if p == 1:
            print(blocks[0])
        stdout.write("\r%d pages scraped" % p)
        stdout.flush()

        if p % 10 == 0:
            with open(baseDir + "/Data/OtherChains/vertcoin/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 10:
                    # if this is the first 20 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/vertcoin/blocks.txt", "a") as logfile:
                logfile.write("%d pages scraped\n" % p)

            blocks = []
        p += 1
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/vertcoin/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/vertcoin/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()