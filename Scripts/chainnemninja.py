from six.moves import urllib
import json
from etherscan import baseDir
from etherscan_utils import getHtml
from bs4 import BeautifulSoup
import csv
from sys import stdout
import time
from datetime import datetime

def scrapePageOfBlocks(height, headers):
    url = "http://chain.nem.ninja/api3/blocks?height=" + str(height)
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    blocks = json.load(response)

    return list(map(lambda b: {
        "Height": b["height"],
        "Hash": b["hash"],
        "Timestamp": b["timestamp"],
        "Transactions": b["tx_count"],
        "Difficulty": b["difficulty"],
        "Fees": float("0." + str(b["fees"]))
    }, blocks))

def scrapeBlocks():
    blocks = []
    height = 2503476
    p = 1
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }
    while height > 0:
        blocks += scrapePageOfBlocks(height, headers)

        stdout.write("\r%d pages of blocks scraped (height %d)" % (p, height))
        stdout.flush()

        if p % 500 == 0:
            with open(baseDir + "/Data/OtherChains/nem/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 500:
                    # if this is the first 500 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/nem/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped (height %d)\n" % (p, height))

            blocks = []

        p += 1
        height -= 25
        time.sleep(0.05)

def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()