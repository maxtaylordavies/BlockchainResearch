import json 
import csv

def main():
    with open("./repos.json") as f:
        coins = json.load(f)
    
    for i in range(len(coins)):
        repoUrls = ["https://github.com/%s/%s" % (coins[i]["org"], repo) for repo in coins[i]["repos"]]
        coins[i] = {
            "Name": coins[i]["name"],
            "Symbol": coins[i]["symbol"],
            "Github repos": repoUrls,
            "Difficulty data source": coins[i]["Difficulty data source"]
        }

    with open("./data_sources.csv", "w+") as dest:
        w = csv.DictWriter(dest, coins[0].keys())
        w.writeheader()
        w.writerows(coins)    

if __name__ == "__main__":
    main()