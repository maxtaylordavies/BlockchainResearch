from sys import stdout, path
path.append("..")

from six.moves import urllib
from datetime import date, datetime
import calendar
import json
from config.config_file import baseDir
import os
from io import StringIO
import csv


def getCoinMetricsAssets():
    url = "https://api.coinmetrics.io/v3/assets"
    headers = {
        "Authorization": "0NOWwq4cUDm1WQF1sEE0"
    }
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    data = json.load(response)
    return data["assets"]


def getExplorerDataForCoin(coin):
    explorerDataDir = os.path.join(baseDir, "Data", "OtherChains")
    folders = os.listdir(explorerDataDir)

    if coin["name"].lower() in folders:
        folder = os.path.join(explorerDataDir, coin["name"].lower())
    elif coin["symbol"].lower() in folders:
        folder = os.path.join(explorerDataDir, coin["symbol"].lower())
    else:
        return False

    if "historical_blocks.csv" not in os.listdir(folder):
        return False

    fn = os.path.join(folder, "historical_blocks.csv")
    with open(fn) as f:
        data = f.read()
        data = data.replace('\x00','?')
        r = csv.DictReader(StringIO(data))
        data = [{k: v for k, v in row.items()}
        for row in r]

    return data


def estimateAddressesFromMiners(coinsToDo):
    with open("repos.json") as f:
        coinList = json.load(f)

    for coin in coinList:
        if coin["name"] not in coinsToDo:
            continue
        explorerData = getExplorerDataForCoin(coin)
        if not explorerData:
            continue
        print(explorerData[0])



    
def coinsToDo():
    notDone = []
    rootDir = os.path.join(baseDir, "Data", "GithubData", "Activity")

    for coin in os.listdir(rootDir):
        if coin == ".DS_Store":
            continue
        fNames = os.listdir(os.path.join(rootDir, coin))    
        if "addresses.json" not in fNames:
            notDone.append(coin)

    return notDone

def parseCoinMetricsObject(obj):
    return {
        "Date": obj["time"][:10],
        "Active addresses": float(obj["values"][0])
    }

def getAddressData(coin):
    data = []

    url = "https://api.coinmetrics.io/v3/assets/%s/metricdata?metrics=AdrActCnt" % coin
    headers = {
        "Authorization": "0NOWwq4cUDm1WQF1sEE0"
    }
    req = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        return []

    data = json.load(response)["metricData"]["series"]
    data = list(map(parseCoinMetricsObject, data))

    return data

def main():
    moneroData = getAddressData("xmr")
    with open(os.path.join(baseDir, "Data", "GithubData", "Activity", "Monero", "addresses.json"), "w+") as f:
        json.dump(moneroData, f, ensure_ascii=False, indent=4)    

    # notDone = coinsToDo()

    # with open("repos.json") as f:
    #     coinList = json.load(f)

    # coins = [c for c in coinList if c["name"] in notDone]
    
    # cmAssets = getCoinMetricsAssets()
    # availableCoins = [c for c in coins if c["symbol"] in cmAssets]

    # print(availableCoins)
    


    # for coin in coinList:
    #     dirpath = os.path.join(baseDir, "Data", "GithubData", "Activity", coin["name"])
    #     symbol = coin["symbol"]

    #     data = getAddressData(symbol)
    #     if data:
    #         print(symbol)
    #         with open(os.path.join(baseDir, "Data", "GithubData", "active-addresses.txt"), "a+") as f:
    #             f.write(coin["name"] + "\n")
    #         with open(os.path.join(dirpath, "addresses.json"), "w+") as f:
    #             json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()