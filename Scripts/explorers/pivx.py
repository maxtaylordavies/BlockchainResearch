from sys import stdout, path
path.append("..")

from config.config_file import baseDir
import csv
import time
from datetime import datetime
from explorers.etherscan_utils import getHtml
from datetime import datetime

def parseDate(dateStr):
    return datetime.strptime(dateStr, "%a, %d %b %Y %H:%M:%S UTC")

def scrapePageOfBlocks(pageNum):
    blocks = []
    url = "https://explorer.pivx.link/blocks?page=%d" % pageNum
    soup = getHtml(url)
   
    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        blocks.append({
            "Height": tds[0].a.string,
            "Hash": tds[1].string,
            "Date": parseDate(tds[2].string),
            "Transactions": float(tds[3].string),
            "Size": float(tds[4].string)
        })

    return blocks

def scrapeBlocks():
    blocks = []
    p = 1
    
    for p in range(1, 44446):
        blocks += scrapePageOfBlocks(p)

        if p == 1:
            print(blocks[0])
        stdout.write("\rscraped page %d" % p)
        stdout.flush()

        if p % 1000 == 0:
            with open(baseDir + "/Data/OtherChains/pivx/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 1000:
                    # if this is the first 1000 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/pivx/blocks.txt", "a") as logfile:
                logfile.write("scraped page %d\n" % p)

            blocks = []
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/pivx/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/pivx/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()