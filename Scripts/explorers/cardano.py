from sys import stdout, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
import csv
import time
from datetime import datetime

def scrapePageOfBlocks(p, headers):
    url = "https://cardanoexplorer.com/api/blocks/pages/?page=%d&pageSize=10" % p
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    response = json.load(response)

    blocks = response["Right"][1]
    return list(map(lambda b: {
        "Epoch": b["cbeEpoch"],
        "Slot": b["cbeSlot"],
        "Height": b["cbeBlkHeight"],
        "Hash": b["cbeBlkHash"],
        "Date": datetime.fromtimestamp(b["cbeTimeIssued"]),
        "Size": b["cbeSize"],
        "Transaction count": b["cbeTxNum"],
        "Total sent": float(b["cbeTotalSent"]["getCoin"]),
        "Fee": float(b["cbeFees"]["getCoin"])
    }, blocks))

def scrapeBlocks():
    blocks = []
    p = 41999
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }

    while p >= 1:
        blocks += scrapePageOfBlocks(p, headers)

        if p == 376060:
            print(blocks[0])
        stdout.write("\rscraped page %d" % p)
        stdout.flush()

        if p % 1000 == 0:
            with open(baseDir + "/Data/OtherChains/cardano/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 1000:
                    # if this is the first 1000 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/cardano/blocks.txt", "a") as logfile:
                logfile.write("scraped page %d\n" % p)

            blocks = []
        p -= 1
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/cardano/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/cardano/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()