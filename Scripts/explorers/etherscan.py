from misc.messari import json2Csv
from sys import stdout, argv
from explorers.etherscan_utils import scrapePageOfBlocks, scrapePageOfForkedBlocks, scrapePageOfTokenTranfers, scrapePageOfTransactions, getTokenContractIds, scrapePageOfTokenTopHolders, getHtml, getTokenInfo, getTokenAnalytics
import json
from datetime import datetime, timedelta
import time
import os
import csv

# baseDir = os.getenv("HOME") + "/BlockchainResearch"
baseDir = os.getenv("HOME") + "/Dropbox/SHARED BLOCKCHAIN PROJECT - DATA/Max Taylor-Davies"

def main():
    if argv[1] == "blocks":
        scrapeAllBlocks()
    elif argv[1] == "forked":
        scrapeAllForkedBlocks()
    elif argv[1] == "transactions":
        scrapeLast24HoursTransactions()
    elif argv[1] == "ids":
        ids = getTokenContractIds()
        with open(baseDir + "/Scripts/ids.json", "w+", encoding="utf-8") as dest:
            json.dump(ids, dest, ensure_ascii=False, indent=4)
    elif argv[1] == "tokens":
        getDataForAllTokens()
    elif argv[1] == "test":
        getTokenAnalytics("0xdac17f958d2ee523a2206206994597c13d831ec7")
    
def getDataForAllTokens():
    with open("/Users/maxtaylordavies/BlockchainResearch/Scripts/ids.json") as tokens:    
        tokens = json.load(tokens)

    for i in range(975, len(tokens)):
        token = tokens[i]
        name = token["name"]
        contract = token["id"]

        stdout.write("\r%d tokens done" % i)
        stdout.flush()
    
        holders = getTopHoldersForToken(contract)
        # info = getTokenInfo(contract)
        # analytics = getTokenAnalytics(contract)

        with open(baseDir + "/Data/TokenData/" + name + "/top_holders.json", "w+", encoding="utf-8") as dest:
            json.dump(holders, dest, ensure_ascii=False, indent=4)
        # with open(baseDir + "/Data/TokenData/" + name + "/info.json", "w+", encoding="utf-8") as dest:
        #     json.dump(info, dest, ensure_ascii=False, indent=4)
        # with open(baseDir + "/Data/TokenData/" + name + "/analytics.json", "w+", encoding="utf-8") as dest:
        #     json.dump(analytics, dest, ensure_ascii=False, indent=4)
        json2Csv(baseDir + "/Data/TokenData/" + name + "/top_holders.json")
        # json2Csv(baseDir + "/Data/TokenData/" + name + "/info.json")
        # json2Csv(baseDir + "/Data/TokenData/" + name + "/analytics.json")
    

def getTopHoldersForToken(contractId):
    holders = []

    url = "https://etherscan.io/token/" + contractId
    soup = getHtml(url)
    cards = soup.findAll("div", {"class": "card-body"})

    div = cards[1].find("div", {"id": "ContentPlaceHolder1_trDecimals"}).find("div", {"class": "col-md-8"})
    decimals = int(div.text.rstrip()) 

    div = cards[0].find("div", {"class": "col-md-8 font-weight-medium"})
    sParam = div.span["title"].replace(" ", "").replace(",", "").split(".")

    if len(sParam) == 2:
        decimals -= len(sParam[1])

    sParam = "".join(sParam) + ("0" * decimals)
 
    for p in range(1, 21):
        h = scrapePageOfTokenTopHolders(contractId, p, sParam)
        if len(h) == 0:
            break
        holders += h        
        time.sleep(0.05)

    return holders

def scrapeAllTransfersForToken(contractId):
    transfers = []
    p = 1

    while True:
        pageOfTransfers = scrapePageOfTokenTranfers(contractId, p)
        if pageOfTransfers == []:
            break

        transfers += pageOfTransfers

        stdout.write("\r%d pages of transfers scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            print("saving")
            # with open(baseDir + "/Data/EtherscanData/Scraping/" + contractId + "_transfers.json", "w+", encoding="utf-8") as dest:
            #     json.dump(transfers, dest, ensure_ascii=False, indent=4)
            # json2Csv(baseDir + "/Data/EtherscanData/Scraping/" + contractId + "_transfers.json")
            with open(baseDir + "/Data/EtherscanData/Scraping/" + contractId + "_transfers.csv", "a") as dest:
                w = csv.DictWriter(dest, transfers[0].keys())
                if not (os.path.isfile("/Data/EtherscanData/Scraping/" + contractId + "_transfers.csv") and os.path.getsize("/Data/EtherscanData/Scraping/" + contractId + "_transfers.csv") > 0):
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(transfers)

            transfers = []
        
        p += 1
        time.sleep(0.2)

    with open(baseDir + "/Data/EtherscanData/Scraping/" + contractId + "_transfers.csv", "a") as dest:
                w = csv.DictWriter(dest, transfers[0].keys())
                if not (os.path.isfile("/Data/EtherscanData/Scraping/" + contractId + "_transfers.csv") and os.path.getsize("/Data/EtherscanData/Scraping/" + contractId + "_transfers.csv") > 0):
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(transfers)

def scrapeLast24HoursTransactions():
    d = datetime.now()
    yesterday = d - timedelta(days=1)
    p = 1
    transactions = []

    while d > yesterday:
        transactions += scrapePageOfTransactions(p)
        p += 1
        d = datetime.strptime(transactions[-1]["Date"], "%Y-%m-%d %H:%M:%S")

        stdout.write("\r%d pages of transactions scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            # we want to save the last 100 pages to disk and then clear the working list to free up RAM
            with open(baseDir + "/Data/EtherscanData/Scraping/transactions.csv", "a") as dest:
                w = csv.DictWriter(dest, transactions[0].keys())
                if os.stat(baseDir + "/Data/EtherscanData/Scraping/transactions.csv").st_size == 0:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(transactions)

            with open(baseDir + "/Logs/transactions.txt", "a") as logfile:
                logfile.write("%d pages of transactions scraped\n" % p)

            transactions = []

        time.sleep(0.25)

    with open(baseDir + "/Data/EtherscanData/Scraping/transactions.csv", "a") as dest:
                w = csv.DictWriter(dest, transactions[0].keys())
                if os.stat(baseDir + "/Data/EtherscanData/Scraping/transactions.csv").st_size == 0:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(transactions)
    

def scrapeAllTransactions():
    transactions = []

    for p in range(1, 5001):
        transactions += scrapePageOfTransactions(p)

        stdout.write("\r%d pages of transactions scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            print("saving")
            with open(baseDir + "/Data/EtherscanData/Scraping/transactions.json", "w+", encoding="utf-8") as dest:
                json.dump(transactions, dest, ensure_ascii=False, indent=4)
            json2Csv(baseDir + "/Data/EtherscanData/Scraping/transactions.json")
        
        time.sleep(0.5)


def scrapeAllBlocks():
    blocks = []

    for p in range(72801, 89764):

        blocks += scrapePageOfBlocks(p)

        stdout.write("\r%d pages of blocks scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            # we want to save the last 100 pages to disk and then clear the working list to free up RAM
            with open(baseDir + "/Data/EtherscanData/Scraping/Blockchain/blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                # if p == 100:
                #     # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                #     w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped\n" % p)

            blocks = []
        
        time.sleep(0.05)


def scrapeLast24HoursBlocks():
    d = datetime.now()
    yesterday = d - timedelta(days=1)
    p = 1
    blocks = []

    while d > yesterday:
        blocks += scrapePageOfBlocks(p)
        p += 1
        d = datetime.strptime(blocks[-1]["Date"], "%Y-%m-%d %H:%M:%S")

        stdout.write("\r%d pages of blocks scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            # we want to save the last 100 pages to disk and then clear the working list to free up RAM
            with open(baseDir + "/Data/EtherscanData/Scraping/blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if os.stat(baseDir + "/Data/EtherscanData/Scraping/blocks.csv").st_size == 0:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            blocks = []

        time.sleep(0.25)

    with open(baseDir + "/Data/EtherscanData/Scraping/blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if os.stat(baseDir + "/Data/EtherscanData/Scraping/blocks.csv").st_size == 0:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)


def scrapeAllForkedBlocks():
    forkedBlocks = []

    for p in range(1, 1113):
        forkedBlocks += scrapePageOfForkedBlocks(p)

        stdout.write("\r%d pages of forked blocks scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            print("saving")
            with open(baseDir + "/Data/EtherscanData/Scraping/forked_blocks.json", "w+", encoding="utf-8") as dest:
                json.dump(forkedBlocks, dest, ensure_ascii=False, indent=4)
            json2Csv(baseDir + "/Data/EtherscanData/Scraping/forked_blocks.json")
        
        time.sleep(0.05)

if __name__== "__main__":
  main()
