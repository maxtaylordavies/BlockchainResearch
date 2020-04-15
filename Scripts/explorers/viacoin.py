from sys import stdout, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
import csv
import time
from datetime import datetime

def scrapePageOfBlocks(date, ts, headers):
    url = "https://explorer.viacoin.org/api/blocks?blockDate=" + date + "&startTimestamp=" + str(ts)
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    data = json.load(response)
    blocks = data["blocks"]

    processedBlocks =  list(map(lambda b: {
        "Height": b["height"],
        "Hash": b["hash"],
        "Time": datetime.fromtimestamp(b["time"]),
        "Timestamp": b["time"],
        "Tx length": b["txlength"]
    }, blocks))

    return (processedBlocks, data["pagination"]["prev"])

def scrapeBlocks():
    blocks = []
    p = 20501
    # ts = 1579883811
    ts = 1488768119
    date = "2017-03-06"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }

    while ts > 1483228800:
        (newBlocks, newDate) = scrapePageOfBlocks(date, ts, headers)

        if not newBlocks:
            date = newDate
        else:
            blocks += newBlocks
            ts = blocks[-1]["Timestamp"]

        stdout.write("\r%d pages of blocks scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            with open(baseDir + "/Data/OtherChains/viacoin/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 100:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/viacoin/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped (next timestamp: %d)\n" % (p, blocks[-1]["Timestamp"]))

            blocks = []

        p += 1
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/viacoin/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/viacoin/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)

    

def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()