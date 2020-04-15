from sys import stdout, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
from explorers.etherscan_utils import getHtml
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

def parseTimestamp(timeString):
    return datetime.strptime(timeString, "%Y-%m-%dT%H:%M:%SZ")

def scrapePageOfBlocks(url, headers):
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    data = json.load(response)
    blocks = data["_embedded"]["records"]

    processedBlocks = list(map(lambda b: {
        "Height": b["sequence"],
        "Hash": b["hash"],
        "Timestamp": parseTimestamp(b["closed_at"]),
        "Successful Transactions": b["successful_transaction_count"],
        "Failed Transactions": b["failed_transaction_count"],
        "Operation Count": b["operation_count"],
        "Total Coins": float(b["total_coins"]),
        "Fee Pool": float(b["fee_pool"])
    }, blocks))

    nextUrl = data["_links"]["next"]["href"] 
    return (processedBlocks, nextUrl)

def scrapeBlocks():
    blocks = []
    p = 8501
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }
    # url = "https://horizon.stellar.org/ledgers?order=desc&limit=200"
    url = "https://horizon.stellar.org/ledgers?cursor=112403863981522944&limit=200&order=desc"

    while True:
        (newBlocks, url) = scrapePageOfBlocks(url, headers)
        blocks += newBlocks

        if p == 1:
            print("\n", blocks[0])
            print("next page: ", url)

        stdout.write("\r%d pages of blocks scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            with open(baseDir + "/Data/OtherChains/stellar/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 100:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/stellar/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped (url: %s)\n" % (p, url))

            blocks = []

        p += 1
        time.sleep(0.05)

def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()