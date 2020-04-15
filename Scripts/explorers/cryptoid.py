from sys import stdout, argv, path
path.append("..")

from six.moves import urllib
import json
from config.config_file import baseDir
from misc.messari import json2Csv
from pathlib import Path

def getLast1000BlocksForChain(chain, headers, outputDir):
    url = "https://chainz.cryptoid.info/explorer/index.data.dws?coin=" + chain + "&v=1&n=1000"
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    data = json.load(response)["blocks"]
    with open(outputDir + "blocks.json", "w+", encoding="utf-8") as dest:
        json.dump(data, dest, ensure_ascii=False, indent=4)
    json2Csv(outputDir + "blocks.json")

def getRichListForChain(chain, headers, outputDir):
    url = "https://chainz.cryptoid.info/explorer/index.stats.dws?coin=" + chain
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    data = json.load(response)["largestAddresses"]
    with open(outputDir + "rich_list.json", "w+", encoding="utf-8") as dest:
        json.dump(data, dest, ensure_ascii=False, indent=4)
    json2Csv(outputDir + "rich_list.json")

def getTopWalletsForChain(chain, headers, outputDir):
    url = "https://chainz.cryptoid.info/explorer/index.wallets.dws?coin=" + chain
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    data = json.load(response)["wallets"]
    with open(outputDir + "top_wallets.json", "w+", encoding="utf-8") as dest:
        json.dump(data, dest, ensure_ascii=False, indent=4)
    json2Csv(outputDir + "top_wallets.json")

def main():
    chain = argv[1]
    outputDir = baseDir + "/Data/OtherChains/" + chain + "/"
    Path(outputDir).mkdir(exist_ok=True)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }
    getLast1000BlocksForChain(chain, headers, outputDir)
    getRichListForChain(chain, headers, outputDir)
    getTopWalletsForChain(chain, headers, outputDir)

if __name__ == "__main__":
    main()