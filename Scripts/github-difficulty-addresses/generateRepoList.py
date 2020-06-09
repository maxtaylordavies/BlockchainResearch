import json

def main():
    outputFilePath = "./repos.txt"
    with open("./repos.json") as f:
        coins = json.load(f)
    for coin in coins:
        if len(coin["repos"]) > 0:
            with open(outputFilePath, "a+") as f:
                f.write("%s: https://www.github.com/%s/%s\n" % (coin["name"], coin["org"], coin["repos"][0]))
    

if __name__ == "__main__":
    main()