from sys import stdout, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
import csv
import time
from datetime import datetime

def scrapePageOfBlocks(hi, headers):
    url = f"https://mainnet.eos.dfuse.io/v0/blocks?skip={hi}&limit=100"
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    blocks = json.load(response)

    return list(map(lambda b: {
        "Height": b["block_num"],
        "Id": b["id"],
        "Date": b["header"]["timestamp"],
        "Producer": b["header"]["producer"],
        "Transactions": b["transaction_count"]
    }, blocks))

def scrapeBlocks():
    blocks = []
    p = 187201
    hi = 122750352 - ((p-1) * 100)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0",
        "Authorization": "Bearer eyJhbGciOiJLTVNFUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1OTExNzk0OTUsImp0aSI6ImQ0YjFiMmFhLWM5YmMtNDlmYi04YTI3LWYyNmQ2Njg0NWJiNSIsImlhdCI6MTU5MTA5MzA5NSwiaXNzIjoiZGZ1c2UuaW8iLCJzdWIiOiJ1aWQ6bWRmdXNlMmY0YzU3OTFiOWE3MzE1IiwidGllciI6ImVvc3EtdjEiLCJ2IjoxLCJ1c2ciOiJ3ZWIiLCJha2kiOiI2OTU0ODU5MDk5MWJjY2ZhYmM2OGZlZDc5MGNiZmU1N2EyYmVkMzg4Y2FiMjg3MDJjNDhmNDE3ZjNjMDQwYWI3Iiwib3JpZ2luIjoibWRmdXNlMmY0YzU3OTFiOWE3MzE1Iiwic3RibGsiOi0zNjAwLCJwbGFuIjowLCJvcHRzIjpbOF19.0nYpsw-rCK0hGbbJxXRdX4Q7IjdH5IQtZVoN7hz5KMEXE3knJGT4cCf6Xif4CRm_cc76zQx7lAjhFG-uGHyysA"
    }

    while hi >= 100:
        newBlocks = scrapePageOfBlocks(hi, headers)
        if not newBlocks:
            break
        blocks += newBlocks

        if p == 1:
            print(blocks[0])
        stdout.write("\r%d pages scraped" % p)
        stdout.flush()

        if p % 10 == 0:
            with open(baseDir + "/Data/OtherChains/eos/historical_blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 10:
                    # if this is the first 20 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/eos/blocks.txt", "a") as logfile:
                logfile.write("%d pages scraped\n" % p)

            blocks = []
        p += 1
        time.sleep(0.1)
    
    with open(baseDir + "/Data/OtherChains/eos/historical_blocks.csv", "a") as dest:
        w = csv.DictWriter(dest, blocks[0].keys())
        w.writerows(blocks)

    with open(baseDir + "/Logs/eos/blocks.txt", "a") as logfile:
        logfile.write("%d pages of blocks scraped\n" % p)


def main():
    scrapeBlocks()

if __name__ == "__main__":
    main()