from sys import stdout, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
import csv
import time
from datetime import datetime

def scrapePageOfBlocks(start, end, headers):
    url = "https://nodes.wavesnodes.com/blocks/headers/seq/%d/%d" % (start,end)
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    response = json.load(response)

    return list(map(lambda b: {
        "Height": b["height"],
        "Hash": b["signature"],
        "Version": b["version"],
        "Date": datetime.fromtimestamp(b["timestamp"] / 1000),
        "Size": b["blocksize"],
        "Reward": b["reward"] if "reward" in b else None,
        "Total fee": b["totalFee"],
        "Desired reward": b["desiredReward"] if "desiredReward" in b else None,
        "Transactions": b["transactionCount"]
    }, response))

def scrapeBlocks():
    blocks = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }
    start = 1745564
    end = 1745663
    p = 2001

    while start > 0:
        blocks += scrapePageOfBlocks(start, end, headers)

        if p == 1:
            print(blocks[0])
        stdout.write("\rscraped page %d" % p)
        stdout.flush()

        if p % 100 == 0:
            with open(baseDir + "/Data/OtherChains/waves/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 100:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/waves/blocks.txt", "a") as logfile:
                logfile.write("scraped page %d ([start,end] = [%d,%d])\n" % (p,start,end))

            blocks = []

        start -= 100
        end -= 100
        p += 1
        
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/waves/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/waves/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()