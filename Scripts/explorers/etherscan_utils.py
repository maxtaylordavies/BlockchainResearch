from bs4 import BeautifulSoup
from coingecko import getDesiredCoinSymbols
from misc.messari import json2Csv
from six.moves import urllib
from sys import stdout
import json
import time
import os
import re
import js2xml

def getTokenAnalytics(contract):
    analytics = []
    url = "https://etherscan.io/token/token-analytics?m=dark&contractAddress=" + contract + "&a=&lg=en"
    soup = getHtml(url)
    script = soup.findAll("script")[6].text
    parsed = js2xml.parse(script)

    data = parsed.xpath("//var[@name='plotData']/functioncall/arguments/array/array")
    for point in data:
        [y, m, d] = point.xpath(".//arguments/number/@value")
        date = y + "-" + m + "-" + d
        stats = point.xpath("./number/@value")
        analytics.append({
            "Date": date,
            "Transfer Amount": stats[0],
            "Transfers Count": stats[1],
            "Unique Receivers": stats[2],
            "Unique Senders": stats[3],
            "Total Uniques": stats[4]
    })
    
    return analytics
    


def isErrorPage(soup):
    h1 = soup.find("h1")
    if h1 == None:
        return False
    return h1.span.string == "Sorry!"

def getTokenInfo(contract):
    info = {}

    url = "https://etherscan.io/token/" + contract + "#tokenInfo"
    soup = getHtml(url)
    div = soup.find("div", {"id": "tokenInfo"})
    rows = div.findAll("tr")

    for row in rows:
        tds = row.findAll("td")
        if len(tds) == 3:
            info[tds[0].string] = tds[2].string

    return info

def getTokenContractIds():
    contractIds = []

    for p in range(1, 11):
        url = "https://etherscan.io/tokens?ps=100&p=" + str(p)
        soup = getHtml(url)
        rows = soup.findAll("tr")[1:]
        for row in rows:
            tds = row.findAll("td")
            link = tds[1].div.div.h3.a
            s = link.string 

            regexResult = re.search("(?<=\().+?(?=\))", s)
            if regexResult != None:
                symbol = regexResult.group()
                name = s.replace(" ("+symbol+")", "")
            else:
                name = s
                symbol = s

            contractId = link["href"][7:]
            
            contractIds.append({"name": name, "symbol": symbol, "id": contractId})

    return contractIds

def scrapePageOfTokenTopHolders(contractId, p, sParam):
    holders = []
    # https://etherscan.io/token/generic-tokenholders2?m=dark&a=0xdac17f958d2ee523a2206206994597c13d831ec7&s=2023709781106661
    url = "https://etherscan.io/token/generic-tokenholders2?a=" + contractId + "&s=" + sParam + "&p=" + str(p)
    soup = getHtml(url)
    rows = soup.findAll("tr")[1:]

    if len(rows) == 2:
        return holders
    
    for row in rows:
        tds = row.findAll("td")
        holders.append({
            "Rank": tds[0].string,
            "Address": tds[1].span.a.string,
            "Quantity": float("".join(tds[2].string.split(","))),
            "Percentage": float(tds[3].string[:-1])
        })

    return holders

def scrapePageOfTokenTranfers(contractId, p):
    transfers = []
    url = "https://etherscan.io/token/generic-tokentxns2?contractAddress=" + contractId + "&p=" + str(p)
    soup = getHtml(url)

    if isErrorPage(soup):
        return

    # find all the <tr/> html elements - these are table rows
    # (the first one just contains column headers so we discard it)
    rows = soup.findAll("tr")[1:]

    # extract the data from each row of the table
    for row in rows:
        tds = row.findAll("td")
        transfers.append({
            "Hash": tds[0].span.a.string,
            "Date": tds[1].span["title"],
            "From": parseToOrFrom(tds[2]),
            "To": parseToOrFrom(tds[4]),
            "Quantity": float("".join(tds[5].string.split(",")))
        })

    return transfers

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
            "Transactions": int(tds[3].string),
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
        return td.string
    else:
        return int(td.string)

def parseToOrFrom(td):
    link = td.a
    if link.has_attr("title"):
        return link["title"]
    else:
        return link.string