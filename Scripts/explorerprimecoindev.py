from six.moves import urllib
import json
from etherscan import baseDir
from etherscan_utils import getHtml
from bs4 import BeautifulSoup
import csv
from sys import stdout
import time
from datetime import datetime
from moneroblocks import parseTimestamp

def scrapePageOfBlocks(offset):
    blocks = []
    url = "https://explorer.primecoin.dev/blocks?limit=1000&offset=" + str(offset) + "&sort=desc"
    soup = getHtml(url)

    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        blocks.append({
            "Height": int(tds[0].a.string.replace(",","")),
            "Timestamp": parseTimestamp(tds[1].string),
            "Transactions": int(tds[4].string),
            "Size (bytes)": int(tds[6].string.replace(",","")),
            "Weight (wu)": int(tds[7].span.string.replace(",","")),
            "Average fee (xpm)": float(tds[5].span.contents[0].split(" ")[0].replace(",",""))
        })

    if offset == 0:
        print("\n", blocks[0])

    return blocks

    

def scrapeBlocks():
    blocks = []
    offset = 2480000 
    p = 2481

    while offset <= 3525000:
        blocks += scrapePageOfBlocks(offset)

        stdout.write("\r%d pages of blocks scraped (offset %d)" % (p, offset))
        stdout.flush()

        if p % 20 == 0:
            with open(baseDir + "/Data/OtherChains/primecoin/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 20:
                    # if this is the first 500 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/primecoin/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped (offset %d)\n" % (p, offset))

            blocks = []

        p += 1
        offset += 1000
        time.sleep(0.1)

def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()