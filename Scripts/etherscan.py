from messari import json2Csv
from sys import stdout, argv
from etherscan_utils import scrapePageOfBlocks, scrapePageOfForkedBlocks, scrapePageOfTokenTranfers, scrapePageOfTransactions, getTokenContractIds, scrapePageOfTokenTopHolders
import json
from datetime import datetime, timedelta
import time
import os
import csv

baseDir = os.getenv("HOME") + "/BlockchainResearch"

def main():
    if argv[1] == "blocks":
        scrapeAllBlocks()
    elif argv[1] == "transactions":
        scrapeLast24HoursTransactions()


def getTopHoldersForToken(contractId):
    holders = []

    for p in range(1, 21):
        holders += scrapePageOfTokenTopHolders(contractId, p)

        stdout.write("\r%d pages of top holders scraped" % p)
        stdout.flush()

        if p == 20:
            print("saving")
            with open(baseDir + "/Data/EtherscanData/Scraping/" + contractId + "_top_holders.json", "w+", encoding="utf-8") as dest:
                json.dump(holders, dest, ensure_ascii=False, indent=4)
            json2Csv(baseDir + "/Data/EtherscanData/Scraping/" + contractId + "_top_holders.json")
        
        time.sleep(0.2)


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
                w.writerows(transactions)

            transfers = []
        
        p += 1
        time.sleep(0.2)

    with open(baseDir + "/Data/EtherscanData/Scraping/" + contractId + "_transfers.csv", "a") as dest:
                w = csv.DictWriter(dest, transfers[0].keys())
                if not (os.path.isfile("/Data/EtherscanData/Scraping/" + contractId + "_transfers.csv") and os.path.getsize("/Data/EtherscanData/Scraping/" + contractId + "_transfers.csv") > 0):
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(transactions)


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

    for p in range(1, 89338):
        try: 
            blocks += scrapePageOfBlocks(p)
        except:
            pass

        # stdout.write("\r%d pages of blocks scraped" % p)
        # stdout.flush()

        if p % 100 == 0:
            # we want to save the last 100 pages to disk and then clear the working list to free up RAM
            with open(baseDir + "/Data/EtherscanData/Scraping/blocks.csv", "a") as dest:
                w = csv.DictWriter(dest, blocks[0].keys())
                if p == 100:
                    # if this is the first 100 pages, we'll need to write the headers to the csv file, then dump the data
                    w.writeheader()
                w.writerows(blocks)

            with open(baseDir + "/Logs/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped\n" % p)

            blocks = []
        
        time.sleep(0.25)


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

    for p in range(1, 1080):
        forkedBlocks += scrapePageOfForkedBlocks(p)

        stdout.write("\r%d pages of forked blocks scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            print("saving")
            with open(baseDir + "/Data/EtherscanData/Scraping/forked_blocks.json", "w+", encoding="utf-8") as dest:
                json.dump(forkedBlocks, dest, ensure_ascii=False, indent=4)
            json2Csv(baseDir + "/Data/EtherscanData/Scraping/forked_blocks.json")
        
        time.sleep(0.5)

if __name__== "__main__":
  main()
