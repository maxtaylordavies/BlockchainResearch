from bs4 import BeautifulSoup
from messari import json2Csv
from six.moves import urllib
from sys import stdout
import json
import time

def main():
    scrapeAllForkedBlocks()
    
def scrapeAllTransactions():
    transactions = []

    for p in range(1, 5001):
        transactions += scrapePageOfTransactions(p)

        stdout.write("\r%d pages of transactions scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            print("saving")
            with open("../Data/EtherscanData/Scraping/transactions.json", "w+", encoding="utf-8") as dest:
                json.dump(transactions, dest, ensure_ascii=False, indent=4)
            json2Csv("../Data/EtherscanData/Scraping/transactions.json")
        
        time.sleep(0.5)

def scrapeAllBlocks():
    blocks = []

    for p in range(1, 88791):
        blocks += scrapePageOfBlocks(p)

        stdout.write("\r%d pages of blocks scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            print("saving")
            with open("../Data/EtherscanData/Scraping/blocks.json", "w+", encoding="utf-8") as dest:
                json.dump(blocks, dest, ensure_ascii=False, indent=4)
            json2Csv("../Data/EtherscanData/Scraping/blocks.json")
        
        time.sleep(0.5)

def scrapeAllForkedBlocks():
    forkedBlocks = []

    for p in range(1, 1080):
        forkedBlocks += scrapePageOfForkedBlocks(p)

        stdout.write("\r%d pages of forked blocks scraped" % p)
        stdout.flush()

        if p % 100 == 0:
            print("saving")
            with open("../Data/EtherscanData/Scraping/forked_blocks.json", "w+", encoding="utf-8") as dest:
                json.dump(forkedBlocks, dest, ensure_ascii=False, indent=4)
            json2Csv("../Data/EtherscanData/Scraping/forked_blocks.json")
        
        time.sleep(0.5)

def scrapePageOfTransactions(pageNum):
    transactions = []
    url = "https://etherscan.io/txs?ps=100&p=" + str(pageNum)
    soup = getHtml(url)

    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        links = row.findAll("a")
        transactions.append({
            "Hash": links[0].string,
            "Date": row.find("td", {"class": "showAge"}).span["title"],
            "Block": links[1].string,
            "From": links[2].string,
            "To": links[3].string, 
            "Value": parseValue(row),
            "Fee": parseFee(row),
        })

    return transactions

def scrapePageOfBlocks(pageNum):
    blocks = []
    url = "https://etherscan.io/blocks?ps=100&p=" + str(pageNum)
    soup = getHtml(url)
   
    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        blocks.append({
            "Block": tds[0].a.string,
            "Date": tds[2].span["title"],
            "Transactions": parseTransactionsNumber(tds[3]),
            "Uncles": int(tds[4].string),
            "Miner name": parseMinerName(tds[5]),
            "Miner address": parseMinerAddress(tds[5]), 
            "Gas used": int("".join(tds[6].contents[0].split(","))),
            "Gas limit": int("".join(tds[7].string.split(","))),
            "Average gas price (Gwei)": parseAverageGasPrice(tds[8].string.split()[0]),
            "Reward (Ether)": parseReward(tds[9]) 
        })

    return blocks
    
def scrapePageOfForkedBlocks(pageNum):
    forkedBlocks = []
    url = "https://etherscan.io/blocks_forked?ps=100&p=" + str(pageNum)
    soup = getHtml(url)

    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        forkedBlocks.append({
            "Height": tds[0].a.string,
            "Date": tds[2].span["title"],
            "Transactions": parseTransactionsNumber(tds[3]),
            "Uncles": int(tds[4].string),
            "Miner name": parseMinerName(tds[5]),
            "Miner address": parseMinerAddress(tds[5]), 
            "Gas limit": int("".join(tds[6].string.split(","))),
            "Difficulty (TH)": float("".join(tds[7].string.split()[0].split(","))),
            "Reward (Ether)": parseReward(tds[8]),
            "Reorg depth": parseReorgDepth(tds[9]) 
        })

    return forkedBlocks

def getHtml(url):
    # make etherscan think we're a browser instead of a python script; otherwise we'll be blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }

    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)

    # load the html into BeautifulSoup
    return BeautifulSoup(response.read(), "html.parser")

# this needs its own function, since the html is structured differently depending on 
# whether the value is an integer or not
def parseValue(row):
    cont = row.findAll("td")[-2].contents
    if len(cont) == 1:
        valueStr = "".join(cont[0].split()[0].split(","))
    elif len(cont) == 4:
        valueStr = "".join(cont[0].split(",")) + cont[1].string + cont[2].string
    else:
        valueStr = "0.0"
    return float(valueStr)
 
def parseFee(row):
    span = row.findAll("td")[-1].span
    cont = span.contents
    if len(cont) == 3:
        feeStr = cont[0] + cont[1].string + cont[2]
    else:
        feeStr = cont[0]
    return float(feeStr)

def parseAverageGasPrice(str):
    if str == "-":
        avg = 0.0
    else:
        avg = float("".join(str.split(",")))
    return avg

def parseReward(td):
    cont = td.contents
    if len(cont) == 1:
        valueStr = cont[0].split()[0]
    elif len(cont) == 3:
        valueStr = cont[0] + cont[1].string + cont[2].string.split()[0]
    else:
        valueStr = "0.0"
    return float(valueStr)

def parseTransactionsNumber(td):
    a = td.a
    if a != None:
        num = int(a.string)
    else:
        num = 0
    return num

def parseMinerAddress(td):
    link = td.a
    return link["href"].split("/")[2]

def parseMinerName(td):
    link = td.a
    try:
        if link.string == link["href"].split("/")[2]:
            name = ""
        else:
            name = link.string
        return name
    except:
        return ""

def parseReorgDepth(td):
    if td.string == "-":
        return 0
    else:
        return int(td.string)


# def getEthereumNodeStats(baseApiUrl, key):
#     url = baseApiUrl + "?module=stats&action=chainsize&startdate=2017-01-01&enddate=2019-10-28&clienttype=geth&syncmode=default&sort=asc&apikey=" + key
#     response = urllib.request.urlopen(url)
#     data = json.load(response)
#     with open("../Data/EtherscanData/nodes.json", "w+", encoding="utf-8") as dest:
#         json.dump(data, dest, ensure_ascii=False, indent=4)
#     json2Csv("../Data/EtherscanData/nodes.json", key="result")


if __name__== "__main__":
  main()
