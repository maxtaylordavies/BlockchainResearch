from messari import json2Csv
from six.moves import urllib
import json

def main():
    baseApiUrl = "https://api.etherscan.io/api"
    key = "6Q2WQJTA6NWGC7UWC95TPA5XRF31CX89RB"

    getEthereumNodeStats(baseApiUrl, key)

def getEthereumNodeStats(baseApiUrl, key):
    url = baseApiUrl + "?module=stats&action=chainsize&startdate=2017-01-01&enddate=2019-10-28&clienttype=geth&syncmode=default&sort=asc&apikey=" + key
    response = urllib.request.urlopen(url)
    data = json.load(response)
    with open("../Data/EtherscanData/nodes.json", "w+", encoding="utf-8") as dest:
        json.dump(data, dest, ensure_ascii=False, indent=4)
    json2Csv("../Data/EtherscanData/nodes.json", key="result")

if __name__== "__main__":
  main()
