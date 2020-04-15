from sys import stdout, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
import csv
import time
from datetime import datetime

def scrapePageOfBlocks(p, headers):
    url = "https://api.iconwat.ch/blocks/?page=%d&count=100" % p
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    response = json.load(response)

    blocks = response["blocks"]
    return list(map(lambda b: {
        "Height": b["height"],
        "Hash": b["hash"],
        "Date": datetime.fromtimestamp(b["timestamp"] / 1000000),
        "Transaction count": b["txCount"],
        "Value": float(b["value"]),
        "Fee": float(b["fee"]),
        "Producer": b["producer"]
    }, blocks))

def scrapeBlocks():
    blocks = []
    headers = {
        # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

    for p in range(81901, 151442) :
        blocks += scrapePageOfBlocks(p, headers)

        if p == 1:
            print(blocks[0])
        stdout.write("\rscraped page %d" % p)
        stdout.flush()

        if p % 100 == 0:
            with open(baseDir + "/Data/OtherChains/icon/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 100:
                    # if this is the first 1000 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/icon/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped\n" % p)

            blocks = []
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/icon/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/icon/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()