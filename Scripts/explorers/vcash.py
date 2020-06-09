from sys import stdout, path
import requests
path.append("..")

from explorers.etherscan_utils import getHtml
from datetime import datetime, timedelta
import time
import os
import csv
from config.config_file import baseDir

def getDateFromAge(ageStr):
    age = [int(x[:-1]) for x in ageStr.split()]
    if "d" in ageStr:
        delta = timedelta(days=age[0], hours=age[1], minutes=age[2])
    elif "h" in ageStr:
        delta = timedelta(hours=age[0], minutes=age[1], seconds=age[2])
    else:
        delta = timedelta(minutes=age[0], seconds=age[1])
    
    date = datetime.now() - delta
    return date.strftime("%Y-%m-%d %H:%M:%S")
        

def scrapePageOfBlocks(p):
    blocks = []
    url = f"https://vcash.tech/?page={p}"
    soup = getHtml(url)
   
    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        blocks.append({
            "Height": int(tds[0].a.string),
            "Hash": tds[1].a.font.string,
            "Date": getDateFromAge(tds[2].string), 
            "Difficulty": float(tds[3].string.replace(",", "")),
            "Reward": float(tds[4].string),
            "Kernels": int(tds[5].string),
            "TokenKernels": int(tds[6].string)
        })

    if p == 1:
        print("\n", blocks[0])

    return blocks

def scrapeAllBlocks():
    blocks = []
    for p in range(601, 3000):
        blocks += scrapePageOfBlocks(p)

        stdout.write("\r%d pages of blocks scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            # we want to save the last 5 pages to disk and then clear the working list to free up RAM
            with open(baseDir + "/Data/OtherChains/vcash/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 100:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/vcash/blocks.txt", "a") as logfile:
                logfile.write(f"{p} pages of blocks scraped\n")

            blocks = []
        
        time.sleep(0.05)

def main():
    scrapeAllBlocks()

if __name__ == "__main__":
    main()