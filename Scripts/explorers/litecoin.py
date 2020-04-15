from sys import stdout, path
path.append("..")

from config.config_file import baseDir
from explorers.etherscan_utils import getHtml
import csv
import time
from datetime import datetime

def scrapePageOfBlocks(p):
    blocks = []
    url = "https://litecoinblockexplorer.net/blocks?page=%d" % p    
    soup = getHtml(url)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        blocks.append({
            "Height": tds[0].a.string,
            "Hash": tds[1].string,
            "Date": datetime.strptime(tds[2].string, "%a, %d %b %Y %H:%M:%S UTC"),
            "Transactions": float(tds[3].string),
            "Size": float(tds[4].string)
        })

    return blocks

def scrapeBlocks():
    blocks = []

    for p in range(17601,35959):
        blocks += scrapePageOfBlocks(p)

        if p == 1:
            print(blocks[0])

        stdout.write("\rscraped page %d" % p)
        stdout.flush()

        if p % 500 == 0:
            with open(baseDir + "/Data/OtherChains/litecoin/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 500:
                    # if this is the first 500 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/litecoin/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped" % p)

            blocks = []
        p += 1
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/litecoin/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/litecoin/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()