from sys import stdout, path
import requests
path.append("..")

from explorers.etherscan_utils import getHtml
from datetime import datetime
import time
import os
import csv
from config.config_file import baseDir

def scrapePageOfBlocks(p):
    blocks = []
    url = f"https://vechainthorscan.com/blocks?page={p}"
    soup = getHtml(url)
   
    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        blocks.append({
            "Height": int(tds[0].a.string),
            "Date": tds[1].span.string, 
            "Transactions": tds[2].string,
            "Clauses": tds[3].string,
            "% Gas used": float(tds[4].div.div.string[:-1]),
            "Gas limit": float(tds[5].string.replace(",","")),
            "VTHO Burned": float(tds[6].string[:-5].replace(",","")),
            "Signer": tds[7].a["href"][9:]
        })

    if p == 0:
        print("\n", blocks[0])

    return blocks

def scrapeAllBlocks():
    blocks = []
    for p in range(114551, 117595):
        blocks += scrapePageOfBlocks(p)

        stdout.write("\r%d pages of blocks scraped" % p)
        stdout.flush()

        if p % 50 == 0 and p != 0:
            # we want to save the last 5 pages to disk and then clear the working list to free up RAM
            with open(baseDir + "/Data/OtherChains/vechain/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 50:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/vechain/blocks.txt", "a") as logfile:
                logfile.write(f"{p} pages of blocks scraped\n")

            blocks = []
        
        time.sleep(0.3)

def main():
    scrapeAllBlocks()

if __name__ == "__main__":
    main()