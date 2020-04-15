from sys import stdout, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
import csv
import time
from datetime import datetime, date, timedelta

def scrapePageOfBlocks(dateStr, headers):
    url = "https://qtum.info/api/blocks?date=%s" % dateStr
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    response = json.load(response)

    return list(map(lambda b: {
        "Height": b["height"],
        "Hash": b["hash"],
        "Date": datetime.fromtimestamp(b["timestamp"]),
        "Interval": b["interval"],
        "Size": b["size"],
        "Transaction count": b["transactionCount"],
        "Miner": b["miner"],
        "Reward": float(b["reward"])
    }, response))

def scrapeBlocks():
    blocks = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }
    dateStr = "2020-02-24"
    p = 1

    while dateStr != "2017-10-01":
        blocks += scrapePageOfBlocks(dateStr, headers)

        if p == 1:
            print(blocks[0])
        stdout.write("\rscraped page %d" % p)
        stdout.flush()

        if p % 50 == 0:
            with open(baseDir + "/Data/OtherChains/qtum/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 50:
                    # if this is the first 1000 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/qtum/blocks.txt", "a") as logfile:
                logfile.write("scraped page %d\n" % p)

            blocks = []

        p += 1
        d = datetime.strptime(dateStr, "%Y-%m-%d").date()
        d -= timedelta(days=1)
        dateStr = d.strftime("%Y-%m-%d")

        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/qtum/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/qtum/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()