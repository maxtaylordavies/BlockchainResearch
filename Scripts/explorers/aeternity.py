from sys import stdout, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
import csv
import time
from datetime import datetime

def scrape500Blocks(start, stop, headers):
    url = "https://mainnet.aeternity.io/middleware/generations/" + str(start) + "/" + str(stop) 
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    data = json.load(response)
    blocks = list(data["data"].values())

    return list(map(lambda b: {
        "Height": b["height"],
        "Hash": b["hash"],
        "Time": datetime.fromtimestamp(b["time"] // 1000),
        "Miner": b["miner"],
        "Version": b["version"]
    }, blocks))

def scrapeBlocks():
    blocks = []
    start = 202786
    stop = 203286
    itr = 1
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }

    while start > 0:
        blocks += scrape500Blocks(start, stop, headers)

        if itr == 1:
            print(blocks[0])

        stdout.write("\r%d iterations" % itr)
        stdout.flush()

        if itr % 20 == 0:
            with open(baseDir + "/Data/OtherChains/aeternity/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if itr == 20:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/aeternity/blocks.txt", "a") as logfile:
                logfile.write("%d itrs scraped (start: %d)\n" % (itr, start))

            blocks = []

        itr += 1
        stop -= 501
        start -= 501
        time.sleep(0.1)
    
    with open(baseDir + "/Data/OtherChains/aeternity/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/aeternity/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % itr)

    

def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()