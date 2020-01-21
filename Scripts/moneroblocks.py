from etherscan import baseDir
from etherscan_utils import getHtml
from bs4 import BeautifulSoup
import csv
from sys import stdout
import time
from datetime import datetime


def parseTimestamp(timeString):
    return datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S")


def scrapeBlocks():
    blocks = []
    p = 20501
    height = 986347

    while height > 1:
        blocks += scrapePageOfBlocks(height)

        stdout.write("\r%d pages of blocks scraped (height %d)" % (p, height))
        stdout.flush()

        if p % 500 == 0:
            with open(baseDir + "/Data/OtherChains/xmr/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 500:
                    # if this is the first 500 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/xmr/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped (height %d)\n" % (p, height))

            blocks = []

        p += 1
        height -= 50
        time.sleep(0.05)


def scrapePageOfBlocks(height):
    blocks = []

    url = "https://moneroblocks.info/browser/" + str(height)
    soup = getHtml(url)
    rows = soup.findAll("div", {"class": "row show-grid top-row"})

    for row in rows:
        columns = row.findAll("div")
        blocks.append({
            "Height": int(columns[0].strong.string),
            "Hash": columns[4].string,
            "Timestamp": parseTimestamp(columns[3].string),
            "Transactions": int(columns[2].string),
            "Size": int(columns[1].string),
        })

    return blocks


def main():
    scrapeBlocks()


if __name__ == "__main__":
    main()