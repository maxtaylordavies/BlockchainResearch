from sys import stdout, argv
from six.moves import urllib
import json
from etherscan import baseDir
from messari import json2Csv

def getLast1000BlocksForChain(chain, outputDir):
    url = "https://chainz.cryptoid.info/explorer/index.data.dws?coin=" + chain + "&v=1&n=1000"
    response = urllib.request.urlopen(url)
    data = json.load(response)
    with open(outputDir + "blocks.json", "w+", encoding="utf-8") as dest:
        json.dump(data, dest, ensure_ascii=False, indent=4)
    json2Csv(outputDir + "blocks.json")

def getRichListForChain(chain, outputDir):
    url = "https://chainz.cryptoid.info/explorer/index.stats.dws?coin=" + chain
    response = urllib.request.urlopen(url)
    data = json.load(response)["largestAddresses"]
    with open(outputDir + "rich_list.json", "w+", encoding="utf-8") as dest:
        json.dump(data, dest, ensure_ascii=False, indent=4)
    json2Csv(outputDir + "blocks.json")

def getTopWalletsForChain(chain, outputDir):
    url = "https://chainz.cryptoid.info/explorer/index.wallets.dws?coin=" + chain
    response = urllib.request.urlopen(url)
    data = json.load(response)["wallets"]
    with open(outputDir + "top_wallets.json", "w+", encoding="utf-8") as dest:
        json.dump(data, dest, ensure_ascii=False, indent=4)
    json2Csv(outputDir + "blocks.json")

def main():
    chain = argv[1]
    outputDir = baseDir + "/Data/OtherChains/" + chain + "/"
    getLast1000BlocksForChain(chain, outputDir)
    getRichListForChain(chain, outputDir)
    getTopWalletsForChain(chain, outputDir)

if __name__ == "__main__":
    main()