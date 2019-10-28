from six.moves import urllib
from coingecko import getDesiredCoinSymbols
import json

def main():
    baseApiUrl = "https://pro-api.coinmarketcap.com/v1/"
    key = "41a99f2d-b542-4d07-99d2-d64facbd3708"

    getMap(baseApiUrl, key)
    
def getMap(baseApiUrl, key):
    symbolsList = getDesiredCoinSymbols()
    symbolsString = ",".join(symbolsList).upper()

    url = baseApiUrl + "cryptocurrency/map?symbol=" + symbolsString
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": key,
    }
    req = urllib.request.Request(url, headers=headers)

    response = urllib.request.urlopen(req)
    data = json.load(response)
    return data["data"]

if __name__== "__main__":
  main()