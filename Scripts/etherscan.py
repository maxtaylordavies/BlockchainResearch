from bs4 import BeautifulSoup
from messari import json2Csv
from six.moves import urllib
import json

def main():
    scrapeAllTransactions()
    

def scrapeAllTransactions():
    transactions = []

    for p in range(1, 11):
        transactions += scrapePageOfTransactions(p)

    with open("../Data/EtherscanData/Scraping/transactions.json", "w+", encoding="utf-8") as dest:
        json.dump(transactions, dest, ensure_ascii=False, indent=4)

    json2Csv("../Data/EtherscanData/Scraping/transactions.json")


def scrapePageOfTransactions(pageNum):
    transactions = []

    url = "https://etherscan.io/txs?p=" + str(pageNum)

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


# this needs its own function, since the html is structured differently depending on 
# whether the value is an integer or not
def parseValue(row):
    cont = row.findAll("td")[-2].contents
    if len(cont) == 1:
        valueStr = cont[0].split()[0]
    elif len(cont) == 4:
        valueStr = cont[0] + cont[1].string + cont[2].string
    else:
        valueStr = "0.0"
    return float(valueStr)
 

def parseFee(row):
    span = row.findAll("td")[-1].span
    feeStr = span.contents[0] + span.contents[1].string + span.contents[2]
    return float(feeStr)


# def getEthereumNodeStats(baseApiUrl, key):
#     url = baseApiUrl + "?module=stats&action=chainsize&startdate=2017-01-01&enddate=2019-10-28&clienttype=geth&syncmode=default&sort=asc&apikey=" + key
#     response = urllib.request.urlopen(url)
#     data = json.load(response)
#     with open("../Data/EtherscanData/nodes.json", "w+", encoding="utf-8") as dest:
#         json.dump(data, dest, ensure_ascii=False, indent=4)
#     json2Csv("../Data/EtherscanData/nodes.json", key="result")


if __name__== "__main__":
  main()
