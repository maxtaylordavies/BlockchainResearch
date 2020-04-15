from sys import stdout, path
path.append("..")

from explorers.etherscan_utils import getHtml
from datetime import datetime
import time
import os
import csv
from config.config_file import baseDir

def parseTimestamp(timeString):
    return datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S")

def scrapePageOfBlocks(hi, p):
    blocks = []
    url = "https://abe.dash.org/chain/Dash?hi=%d&count=1000" % hi
    soup = getHtml(url)
   
    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        blocks.append({
            "Height": int(tds[0].a.string),
            "Timestamp": parseTimestamp(tds[1].string),
            "Transactions": int(tds[2].string),
            "Value": float(tds[3].string),
            "Difficulty": float(tds[4].string),
            "Outstanding": float(tds[5].string),
            "Chain age": float(tds[7].string),
            "% CoinDD": float(tds[8].string[:-1]) if tds[8].string != '' else None 
        })

    if p == 1:
        print("\n", blocks[0])

    return blocks

def scrapeAllBlocks():
    blocks = []
    hi = 23619
    p = 12001
    while hi > 0:

        blocks += scrapePageOfBlocks(hi, p)

        stdout.write("\r%d pages of blocks scraped" % p)
        stdout.flush()

        if p % 50 == 0:
            # we want to save the last 100 pages to disk and then clear the working list to free up RAM
            with open(baseDir + "/Data/OtherChains/dash/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 50:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/dash/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped\n" % p)

            blocks = []
        
        time.sleep(0.05)
        hi -= 1000
        p += 1

def main():
    scrapeAllBlocks()

if __name__ == "__main__":
    main()