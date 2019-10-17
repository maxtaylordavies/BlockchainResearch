import json
from six.moves import urllib

def main():
    # get market data
    getData("https://data.messari.io/api/v1/markets", "./MessariData/MarketsData.json")
    # get asset data
    getData("https://data.messari.io/api/v1/assets", "./MessariData/AssetData.json")

def getData(url, outputFile):
    response = urllib.request.urlopen(url)
    data = json.load(response)
    with open(outputFile, "w+") as dest:
        json.dump(data, dest)

if __name__== "__main__":
  main()