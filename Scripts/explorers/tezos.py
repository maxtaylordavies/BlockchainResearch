from sys import stdout, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
import csv
import time
from datetime import datetime

def scrapePageOfBlocks(start, headers):
    url = f"https://node1.sg.tezos.org.sg/tables/block?columns=height,time,hash,n_ops,baker,row_id&limit=20&row_id.rg={start},{start+19}"
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    blocks = json.load(response)

    return list(map(lambda b: {
        "Height": b[0],
        "Date": datetime.fromtimestamp(b[1] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
        "Hash": b[2],
        "Operations": b[3],
        "Baker": b[4]
    }, blocks))

def scrapeBlocks():
    blocks = []
    headers = {
        # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

    p = 43401
    start = 948186 - (20 * (p - 1))
    while start > 0:
        blocks += scrapePageOfBlocks(start, headers)

        if p == 1:
            print(blocks[0])
        stdout.write("\rscraped page %d" % p)
        stdout.flush()

        if p % 100 == 0:
            with open(baseDir + "/Data/OtherChains/tezos/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 100:
                    # if this is the first 1000 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/tezos/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped\n" % p)

            blocks = []

        p += 1
        start -= 20    
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/tezos/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/tezos/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()