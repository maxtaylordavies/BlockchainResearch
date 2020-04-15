from sys import stdout, path
path.append("..")

from config.config_file import baseDir
import csv
import time
from datetime import datetime
from explorers.etherscan_utils import getHtml
from datetime import datetime

def parseDate(td):
    dateStr = td.div["data-original-title"]
    return datetime.strptime(dateStr, "%-d/%m/%Y %-I:%M:%S %p")

def scrapePageOfBlocks(p):
    blocks = []
    url = "https://viewblock.io/zilliqa/blocks?page=%d" % p
    soup = getHtml(url)
   
    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        blocks.append({
            "Height": tds[0].a.string,
            "Date": parseDate(tds[1]),
            "Transactions": float(tds[2].string),
            "DS Leader": tds[3].string,
            "Reward": float(tds[4].string.split(" ")[0]),
            "DS Block": int(tds[5].string)
        })

    return blocks

def scrapeBlocks():
    blocks = []
    p = 1
    
    for p in range(1, 17851):
        blocks += scrapePageOfBlocks(p)

        if p == 1:
            print(blocks[0])
        stdout.write("\rscraped page %d" % p)
        stdout.flush()

        if p % 1000 == 0:
            with open(baseDir + "/Data/OtherChains/zilliqa/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 1000:
                    # if this is the first 1000 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/zilliqa/blocks.txt", "a") as logfile:
                logfile.write("scraped page %d\n" % p)

            blocks = []
        time.sleep(0.05)
    
    with open(baseDir + "/Data/OtherChains/zilliqa/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/zilliqa/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()