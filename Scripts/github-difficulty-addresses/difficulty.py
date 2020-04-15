from sys import stdout, path
path.append("..")

import json
from datetime import date, datetime
import calendar
from six.moves import urllib
from config.config_file import baseDir
import os
import csv
from statistics import mean
import pandas as pd
import codecs
from io import StringIO
from statistics import mean
from misc.messari import json2Csv

def parseCoinMetricsObject(obj):
    return {
        "Date": obj["time"][:10],
        "Average difficulty": float(obj["values"][0])
    }

def getDifficultyDataFromExistingFile(fn):
    with open(fn) as f:
        data = f.read()
        data = data.replace('\x00','?')
        r = csv.DictReader(StringIO(data))
        data = [{k: v for k, v in row.items()}
        for row in r]
    
    if "Time" in data[0]:
        data = [{"Date": d["Time"], "Difficulty": float(d["Difficulty"])} for d in data]
    elif "Date" in data[0]:
        data = [{"Date": d["Date"], "Difficulty": float(d["Difficulty"])} for d in data]
    elif "Timestamp" in data[0]:
         data = [{"Date": d["Timestamp"], "Difficulty": float(d["Difficulty"])} for d in data]

    # ok so no we have list of difficulty values with timestamps. Need to convert this to daily average. 
    dailyData = {}
    for point in data:
        dateStr = point["Date"][:10]
        if dateStr in dailyData:
            dailyData[dateStr].append(point["Difficulty"])
        else:
            dailyData[dateStr] = [point["Difficulty"]]
    
    dailyData = [{"Date": k, "Average difficulty": mean(dailyData[k])} for k in dailyData.keys()]
    coin = fn.split("/")[-2].capitalize()

    
    
    w = csv.DictWriter(dest, dailyData[0].keys())
    w.writeheader()
    w.writerows(dailyData)


def existingData():
    files = []
    filesWithDifficultyData = []

    rootDir = os.path.join(baseDir, "Data", "OtherChains")
    for (dirpath, dirnames, filenames) in os.walk(rootDir):
        for fn in filenames:
            if "historical_blocks" in fn:
                fp = os.path.join(dirpath, fn)
                files.append(fp)
    
    for filename in files:
        with open(filename) as f:
            reader = csv.reader(f)
            headers = next(reader)
            if "Difficulty" in headers:
                filesWithDifficultyData.append(filename)
    
    for filename in filesWithDifficultyData:
        getDifficultyDataFromExistingFile(filename)
        


def coinmetrics(coins):
    for coin in coins:
        name = coin["name"]
        symbol = coin["symbol"]

        url = "https://api.coinmetrics.io/v3/assets/%s/metricdata?metrics=DiffMean" % symbol

        print(url)

        headers = {
            "Authorization": "0NOWwq4cUDm1WQF1sEE0"
        }
        req = urllib.request.Request(url, headers=headers)

        try:
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError:
            continue

        data = json.load(response)["metricData"]["series"]

        data = list(map(parseCoinMetricsObject, data))
        destPath = os.path.join(baseDir, "Data", "GithubData", "Activity", name, "difficulty.json")
        with open(destPath, "w+") as dest:
            json.dump(data, dest, ensure_ascii=False, indent=4)

        with open(os.path.join(baseDir, "Data", "GithubData", "difficulty.txt"), "a+") as f:
            f.write(name + "\n")
        



def makeDaily(data):
    dailyStats = []
    hashMap = {}
    for entry in data:
        if entry["Date"] in hashMap:
            hashMap[entry["Date"]].append(entry["Average difficulty"])
        else:
            hashMap[entry["Date"]] = [entry["Average difficulty"]]

    averagedHash = {d:mean(hashMap[d]) for d in hashMap}
    for d in averagedHash:
        dailyStats.append({"Date": d, "Average difficulty": averagedHash[d]})       

    return sorted(dailyStats, key=lambda k: datetime.strptime(k["Date"], "%Y-%m-%d"))

def coinwarz():
    # files = []
    # rootDir = "./coinwarz"
    # for (dirpath, dirnames, filenames) in os.walk(rootDir):
    #     for fn in filenames:
    #         fp = os.path.join(dirpath, fn)
    #         files.append(fp)

    files = ["./coinwarz/Fastcoin.json"]
    for fp in files:
        with open(fp) as f:
            rawData = json.load(f)
            data = list(map(lambda x : {"Date": datetime.strftime(datetime.fromtimestamp(x[0] / 1000), "%Y-%m-%d"), "Average difficulty": x[1]}, rawData))
            
            coinName = fp.split("/")[-1].split(".")[0]
            destPath = os.path.join(baseDir, "Data", "GithubData", "Activity", coinName, "difficulty.json")
            
            with open(destPath, "w+") as dest:
                json.dump(data, dest, ensure_ascii=False, indent=4)
            
            with open(os.path.join(baseDir, "Data", "GithubData", "difficulty.txt"), "a+") as f:
                f.write(coinName + "\n")



def coinexplorer():
    url = "https://www.coinexplorer.net/api/DOGE/chartsData/PoWDifficultyPerDay/?_=1584727342572"


def getStats(coin):
    url = "https://chainz.cryptoid.info/explorer/charts/diff.stats.dws?coin=%s&n=0" % coin
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0"
    }
    req = urllib.request.Request(url, headers=headers)

    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        return []

    data = json.load(response)

    n = len(data["dates"])
    for i in range(1, n):
        data["dates"][i] += data["dates"][i-1]
        data["diffs"][i] += data["diffs"][i-1]
        data["minDiffs"][i] += data["minDiffs"][i-1]
        data["maxDiffs"][i] += data["maxDiffs"][i-1]

    stats = []
    for i in range(n):
        stats.append({
            "Date": datetime.fromtimestamp(data["dates"][i]).strftime("%Y-%m-%d %H:%M:%S"),
            # "Date": datetime.fromtimestamp(data["dates"][i]),
            "Average difficulty": 0.01 * ((data["minDiffs"][i] + data["maxDiffs"][i]) / 2) 
        })
    
    return stats

def getDailyStats(stats):
    dailyStats = []

    # get timestamp representing today at 00:00
    today = datetime.today()
    today = date(today.year, today.month, today.day)
    today = calendar.timegm(today.timetuple())

    # get timestamp representing the furthest day back the data goes at 00:00
    startDate = datetime.strptime(stats[0]["Date"], "%Y-%m-%d %H:%M:%S").date()
    limit = calendar.timegm(startDate.timetuple())

    d = today
    while d >= limit:
        dailyStats.append({
            "Date": datetime.utcfromtimestamp(d).strftime("%Y-%m-%d"),
            "Average difficulty": 0
        })
        d -= (60 * 60 * 24)

    for entry in stats:
        el = next((x for x in dailyStats if x["Date"] == entry["Date"][:10]), None)
        if el != None:
            i = dailyStats.index(el)
            dailyStats[i]["Average difficulty"] = entry["Average difficulty"]
            
    for i in range(0, len(dailyStats)-1):
        if dailyStats[i]["Average difficulty"] == 0:
            dailyStats[i]["Average difficulty"] = dailyStats[i+1]["Average difficulty"]

    return dailyStats[::-1]

def main(): 
    # destfp = os.path.join(baseDir, "Data", "GithubData", "Activity", "Netcoin", "difficulty.json")
    # json2Csv(destfp)

    # stats = getStats("glc")
    # dailyStats = getDailyStats(stats)
    # destfp = os.path.join(baseDir, "Data", "GithubData", "Activity", "Goldcoin", "difficulty.json")
    # with open(destfp, "w+") as dest:
    #     json.dump(dailyStats, dest, ensure_ascii=False, indent=4)
    # json2Csv(destfp)

    coinwarz()
            
if __name__ == "__main__":
    main()