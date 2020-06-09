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
    url = f"https://grin.blockscan.com/blocks?p={p}"
    soup = getHtml(url)
   
    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        blocks.append({
            "Height": int(tds[0].a.string),
            "Date": tds[1].span["title"], 
            "Difficulty": float(tds[2].string),
            "Inputs": int(tds[3].a.string),
            "Outputs": int(tds[4].a.string),
            "Kernels": int(tds[5].a.string),
            "PoW": tds[6].string,
            "Reward": tds[7].string,
            "Mining time": tds[8].string
        })

    if p == 1:
        print("\n", blocks[0])

    return blocks

def scrapeAllBlocks():
    blocks = []
    for p in range(19401, 27656):
        blocks += scrapePageOfBlocks(p)

        stdout.write(f"\r{p} pages of blocks scraped ({int(100*(p/27656))}% done)")
        stdout.flush()

        if p % 100 == 0:
            # we want to save the last 5 pages to disk and then clear the working list to free up RAM
            with open(baseDir + "/Data/OtherChains/grin/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 100:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/grin/blocks.txt", "a") as logfile:
                logfile.write(f"{p} pages of blocks scraped\n")

            blocks = []
        
        time.sleep(0.3)

def main():
    scrapeAllBlocks()

if __name__ == "__main__":
    main()