from messari import json2Csv
from sys import stdout, argv
from etherscan_utils import scrapePageOfBlocks, scrapePageOfForkedBlocks, scrapePageOfTokenTranfers, scrapePageOfTransactions, getTokenContractIds, scrapePageOfTokenTopHolders
import json
import time
import os

baseDir = os.getenv("HOME") + "/BlockchainResearch"

def main():
    if sys.argv[1] == "blocks":
        scrapeAllBlocks()

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

    for p in range(1, 4001):
        transfers += scrapePageOfTokenTranfers(contractId, p)

        stdout.write("\r%d pages of transfers scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            print("saving")
            with open(baseDir + "/Data/EtherscanData/Scraping/" + contractId + "_transfers.json", "w+", encoding="utf-8") as dest:
                json.dump(transfers, dest, ensure_ascii=False, indent=4)
            json2Csv(baseDir + "/Data/EtherscanData/Scraping/" + contractId + "_transfers.json")
        
        time.sleep(0.2)
    
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
        blocks += scrapePageOfBlocks(p)

        # stdout.write("\r%d pages of blocks scraped" % p)
        # stdout.flush()

        if p % 100 == 0:
            with open(baseDir + "/Data/EtherscanData/Scraping/blocks.json", "w+", encoding="utf-8") as dest:
                json.dump(blocks, dest, ensure_ascii=False, indent=4)
            # json2Csv(baseDir + "/Data/EtherscanData/Scraping/blocks.json")
            with open(baseDir + "/Logs/blocks.txt", "a") as logfile:
                logfile.write("%d pages of blocks scraped\n" % p)
        
        time.sleep(0.25)

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
