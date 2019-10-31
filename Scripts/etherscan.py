from bs4 import BeautifulSoup
from messari import json2Csv
from six.moves import urllib
import json

def main():
    transactions = scrapeTransactions()
    for t in transactions:
        print(t["Value"])

def scrapeTransactions():
    transactions = []

    url = "https://etherscan.io/txs"

    # make etherscan think we're a browser instead of a python script; otherwise we'll be blocked
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }

    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)

    # load the html into BeautifulSoup
    soup = BeautifulSoup(response.read(), "html.parser")

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

def parseValue(row):
    valueStr = row.findAll("td")[-2].string
    if valueStr != None:
        return float(valueStr.split()[0])
    else:
        return 0.0
 

def parseFee(row):
    span = row.findAll("td")[-1].span
    feeStr = span.contents[0] + span.contents[1].string + span.contents[2]
    return float(feeStr)

def getEthereumNodeStats(baseApiUrl, key):
    url = baseApiUrl + "?module=stats&action=chainsize&startdate=2017-01-01&enddate=2019-10-28&clienttype=geth&syncmode=default&sort=asc&apikey=" + key
    response = urllib.request.urlopen(url)
    data = json.load(response)
    with open("../Data/EtherscanData/nodes.json", "w+", encoding="utf-8") as dest:
        json.dump(data, dest, ensure_ascii=False, indent=4)
    json2Csv("../Data/EtherscanData/nodes.json", key="result")

if __name__== "__main__":
  main()
