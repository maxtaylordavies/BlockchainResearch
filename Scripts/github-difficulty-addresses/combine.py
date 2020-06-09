from sys import stdout, path
path.append("..")

import os
from config.config_file import baseDir
import json
from datetime import datetime
from misc.messari import json2Csv

def stats():
    githubCoins = []
    difficultyCoins = []
    addressesCoins = []

    rootDir = os.path.join(baseDir, "Data", "GithubData", "Activity")

    for coin in os.listdir(rootDir):
        if coin == ".DS_Store":
            continue
        fNames = os.listdir(os.path.join(rootDir, coin))    
        githubFNames = [fn for fn in fNames if fn.endswith("json") and not fn.startswith("difficulty") and not fn.startswith("addresses")]
        if githubFNames:
            githubCoins.append(coin)
        if "difficulty.json" in fNames:
            difficultyCoins.append(coin)
        if "addresses.json" in fNames:
            addressesCoins.append(coin)

    print(len(githubCoins))

    print("Coins we have github data for:")
    for c in githubCoins:
        print(c)

    print("\nCoins we have github + difficulty data for:")
    for c in githubCoins:
        if c in difficultyCoins:
            print(c)
    
    print("\nCoins we have github + difficulty + address data for:")
    for c in githubCoins:
        if c in difficultyCoins and c in addressesCoins:
            print(c)

     



def main():
    # stats()

    rootDir = os.path.join(baseDir, "Data", "GithubData", "Activity")

    for coin in os.listdir(rootDir):
    # for coin in ["Bytecoin", "Clams", "Worldcoin", "Novacoin", "Startcoin", "Fastcoin", "Bullion"]:
        if coin == ".DS_Store":
            continue
        
        # get github data
        fNames = os.listdir(os.path.join(rootDir, coin))
        githubFNames = [fn for fn in fNames if fn.endswith("json") and not fn.startswith("difficulty") and not fn.startswith("addresses")]
        # githubFNames = [coin.lower() + ".json"]

        if not githubFNames:
            continue

        githubFPath = os.path.join(rootDir, coin, githubFNames[0])
        with open(githubFPath) as f:
            githubData = json.load(f)
            githubData = githubData[::-1]

        # get difficulty data if available
        difficultyData = []
        if "difficulty.json" in fNames:
            difficultyFPath = os.path.join(rootDir, coin, "difficulty.json")
            with open(difficultyFPath) as f:
                difficultyData = json.load(f)

        # get active address data if available
        activeAddressData = []
        if "addresses.json" in fNames:
            addressesFPath = os.path.join(rootDir, coin, "addresses.json")
            with open(addressesFPath) as f:
                activeAddressData = json.load(f)

        # find the range of dates for which we have all the stats
        githubStart = githubData[0]["Date"]
        githubEnd = githubData[-1]["Date"]

        difficultyStart = difficultyData[0]["Date"] if difficultyData else githubStart
        difficultyEnd = difficultyData[-1]["Date"] if difficultyData else githubEnd

        addressesStart = activeAddressData[0]["Date"] if activeAddressData else githubStart
        addressesEnd = activeAddressData[-1]["Date"] if activeAddressData else githubEnd

        start = max([datetime.strptime(d, "%Y-%m-%d") for d in (githubStart, difficultyStart, addressesStart)])
        end = min([datetime.strptime(d, "%Y-%m-%d") for d in (githubEnd, difficultyEnd, addressesEnd)])

        # remove entries outside these dates from all the data arrays
        githubData = [x for x in githubData if start <= datetime.strptime(x["Date"], "%Y-%m-%d") <= end]
        difficultyData = [x for x in difficultyData if start <= datetime.strptime(x["Date"], "%Y-%m-%d") <= end]
        activeAddressData = [x for x in activeAddressData if start <= datetime.strptime(x["Date"], "%Y-%m-%d") <= end]

        # merge
        for i in range(len(difficultyData)):
            githubData[i]["Average difficulty"] = difficultyData[i]["Average difficulty"]
        for i in range(len(activeAddressData)):
            githubData[i]["Active addresses"] = activeAddressData[i]["Active addresses"]

        outputPath = os.path.join(baseDir, "Data", "github_difficulty_addresses", coin+".json")
        with open(outputPath, "w+") as f:
            json.dump(githubData, f, ensure_ascii=False, indent=4)
        
        json2Csv(outputPath)





if __name__ == "__main__":
    main()