from sys import stdout, path
import requests
path.append("..")

from explorers.etherscan_utils import getHtml
from datetime import datetime
import time
import os
import csv
from config.config_file import baseDir

def scrapePageOfBlocks(hi):
    blocks = []
    url = f"https://mainnet.decred.org/blocks?height={hi}&rows=100"
    soup = getHtml(url)
   
    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        blocks.append({
            "Height": None if not tds[0].a.string else int(tds[0].a.string),
            "Date": tds[10].text, 
            "Size": tds[7].string,
            "Transactions": int(tds[1].string),
            "Votes": int(tds[2].string),
            "Tickets": int(tds[3].string),
            "Revocations": int(tds[4].string),
            "DCR": tds[6].text,
            "Version": int(tds[8].text)
        })

    if hi == 447366:
        print("\n", blocks[0])

    return blocks

def scrapeAllBlocks():
    blocks = []
    p = 3501
    hi = 447366 - (100 * (p-1))
    while hi > 0:
        blocks += scrapePageOfBlocks(hi)

        stdout.write("\r%d pages of blocks scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            # we want to save the last 5 pages to disk and then clear the working list to free up RAM
            with open(baseDir + "/Data/OtherChains/decred/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 100:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/decred/blocks.txt", "a") as logfile:
                logfile.write(f"{p} pages of blocks scraped\n")

            blocks = []
        
        time.sleep(0.05)
        hi -= 100
        p += 1

def main():
    scrapeAllBlocks()

if __name__ == "__main__":
    main()