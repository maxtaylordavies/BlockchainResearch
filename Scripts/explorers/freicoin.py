from sys import stdout, path
path.append("..")

from explorers.etherscan_utils import getHtml
from datetime import datetime
import time
import os
import csv
from config.config_file import baseDir

def scrapePageOfBlocks(hi):
    blocks = []
    url = f"https://freicoin.info/chain/Freicoin?hi={hi}&count=1000"
    soup = getHtml(url)
   
    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        blocks.append({
            "Height": int(tds[0].a.string),
            "Date": tds[1].string, 
            "Transactions": int(tds[2].string),
            "Value out": float(tds[3].string),
            "Difficulty": float(tds[4].string),
            "Outstanding": float(tds[5].string),
            "Average age": float(tds[6].string),
            "Chain age": float(tds[7].string),
            "% CoinDD":  None if tds[8].string == '' else float(tds[8].string[:-1])
        })

    if hi == 421106:
        print("\n", blocks[0])

    return blocks

def scrapeAllBlocks():
    blocks = []
    p = 271
    hi = 272980 - (1000 * (p-1))
    while hi > 0:
        print(hi)
        blocks += scrapePageOfBlocks(hi)

        stdout.write("\r%d pages of blocks scraped" % p)
        stdout.flush()

        if p % 5 == 0:
            # we want to save the last 5 pages to disk and then clear the working list to free up RAM
            with open(baseDir + "/Data/OtherChains/freicoin/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 5:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/freicoin/blocks.txt", "a") as logfile:
                logfile.write(f"{p} pages of blocks scraped\n")

            blocks = []
        
        time.sleep(0.1)
        hi -= 1000
        p += 1

def main():
    scrapeAllBlocks()

if __name__ == "__main__":
    main()