from sys import path, stdout
path.append("..")

from config.config_file import baseDir
from explorers.etherscan_utils import getHtml
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime


def parseTimestamp(timeString):
    return datetime.strptime(timeString, "%a, %d %b %Y %H:%M:%S %Z")


def scrapeBlocks():
    blocks = []
    for p in range(76001, 202564):
        blocks += scrapePageOfBlocks(p)

        stdout.write("\r%d pages of blocks scraped" % p)
        stdout.flush()

        if p % 500 == 0:
            # we want to save the last 100 pages to disk and then clear the working list to free up RAM
            with open(baseDir + "/Data/OtherChains/dgb/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                # if p == 500:
                #     # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                #     w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/dgb/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped\n" % p)

            blocks = []
        
        time.sleep(0.05)


def scrapePageOfBlocks(pageNum):
    blocks = []
    url = "https://digibyteblockexplorer.com/blocks?page=" + str(pageNum)
    soup = getHtml(url)
   
    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        print(tds)
        blocks.append({
            "Height": int(tds[0].a.string),
            "Hash": tds[1].string,
            "Timestamp": parseTimestamp(tds[2].string),
            "Transactions": int(tds[3].string),
            "Size": int(tds[4].string),
        })

    if pageNum == 1:
        print("\n", blocks[0])

    return blocks


def main():
    scrapeBlocks()


if __name__ == "__main__":
    main()