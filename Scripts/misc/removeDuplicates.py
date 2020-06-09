import csv
from io import StringIO
import os
from collections import OrderedDict

baseDir = os.getenv("HOME") + "/Dropbox/SHARED BLOCKCHAIN PROJECT - DATA/Max Taylor-Davies"

def getLastBlock(coin):
    fn = f"{baseDir}/Data/OtherChains/{coin}/historical_blocks.csv"
    with open(fn) as f:
        data = f.read()
        data = data.replace('\x00','?')
        r = csv.DictReader(StringIO(data))
        data = [{k: v for k, v in row.items()} for row in r]
    print(data[-1])

    fn = f"{baseDir}/Data 2/OtherChains/{coin}/historical_blocks.csv"
    with open(fn) as f:
        data = f.read()
        data = data.replace('\x00','?')
        r = csv.DictReader(StringIO(data))
        data = [{k: v for k, v in row.items()} for row in r]
    print(data[-1])


def removeDupes(coin):
    fn = f"{baseDir}/Data/OtherChains/{coin}/historical_blocks.csv"
    with open(fn) as f:
        data = f.read()
        data = data.replace('\x00','?')
        r = csv.DictReader(StringIO(data))
        data = [{k: v for k, v in row.items()} for row in r]

    result = list(OrderedDict((frozenset(item.items()),item) for item in data).values())

    with open(fn, "w") as dest:
        w = csv.DictWriter(dest, result[0].keys())
        w.writeheader()
        w.writerows(result)    

    print(f"{len(data)-len(result)} duplicates removed for {coin}")

def main():
    folders = os.listdir(f"{baseDir}/Data/OtherChains")
    for folder in folders:
        if folder != ".DS_Store" and "historical_blocks.csv" in os.listdir(f"{baseDir}/Data/OtherChains/{folder}"):
            removeDupes(folder)

if __name__ == "__main__":
    main()