from sys import stdout, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
import csv
import time
from datetime import datetime

def scrapePageOfBlocks(n, headers):
    url = f"https://explorer.lisk.io/api/getLastBlocks?n={n}"
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    response = json.load(response)

    blocks = response["blocks"]
    return list(map(lambda b: {
        "Height": int(b["height"]),
        "Id": b["id"],
        "Date": datetime.fromtimestamp(b["timestamp"]).strftime("%Y-%m-%d %H:%M:%S"),
        "Generator": b["generator"],
        "Total amount": float(b["totalAmount"]),
        "Total fee": float(b["totalFee"]),
        "Reward": float(b["reward"]),
        "Total Forged": float(b["totalForged"]),
        "Transactions": int(b["transactionsCount"]),
        "Delegate address": b["delegate"]["address"],
        "Delegate approval": float(b["delegate"]["approval"]),
        "Delegate missed blocks": int(b["delegate"]["missedblocks"]),
        "Delegate produced blocks": int(b["delegate"]["producedblocks"]),
        "Delegate productivity": float(b["delegate"]["productivity"]),
        "Delegate public key": b["delegate"]["publicKey"],
        "Delegate rate": int(b["delegate"]["rate"]),
        "Delegate username": b["delegate"]["username"],
        "Delegate vote": b["delegate"]["vote"]
    }, blocks))

def scrapeBlocks():
    blocks = []
    headers = {
        # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

    p = 162401
    n = 20 * (p - 1)
    while n < 10000000:
        blocks += scrapePageOfBlocks(n, headers)

        if p == 1:
            print(blocks[0])
        stdout.write("\rscraped page %d" % p)
        stdout.flush()

        if p % 100 == 0:
            with open(baseDir + "/Data/OtherChains/lisk/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 100:
                    # if this is the first 1000 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/lisk/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped\n" % p)

            blocks = []

        p += 1    
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/lisk/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/lisk/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()