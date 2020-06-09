from sys import path, stdout
path.append("..")

from six.moves import urllib
import json
from misc.messari import json2Csv
from datetime import datetime, date
import calendar
import os
import time
from config.config_file import baseDir, githubToken as token


def main():
    with open("./repos.json") as f:
        coins = json.load(f)
    for coin in coins[46:]:
        dirpath = os.path.join(baseDir, "Data", "GithubData", "Activity", coin["name"])
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        logFilePath = os.path.join(dirpath, "log.txt")
        for repo in coin["repos"]:
            print("\nmining activity data for repo %s....." % repo)
            activity = getHistoricalActivityOnRepo(coin["org"], repo, logFilePath)
            destpath = os.path.join(dirpath, repo+".json")
            with open(destpath, "w") as dest:
                json.dump(activity, dest, ensure_ascii=False, indent=4)
            json2Csv(destpath)


def convertJsonFiles():
    commitsDir  = "/Users/maxtaylordavies/Dropbox/SHARED BLOCKCHAIN PROJECT - DATA/Max Taylor-Davies/Data/GithubData/Commits"
    for (dirpath, dirnames, filenames) in os.walk(commitsDir):
        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            print("converting", fn)
            json2Csv(fp)

    forksDir  = "/Users/maxtaylordavies/Dropbox/SHARED BLOCKCHAIN PROJECT - DATA/Max Taylor-Davies/Data/GithubData/Forks"
    for (dirpath, dirnames, filenames) in os.walk(forksDir):
        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            json2Csv(fp)

    
def getHistoricalActivityOnRepo(repoOwner, repoName, logFilePath):
    activity = []
    allCommits = getAllCommitsOnRepo(repoOwner, repoName, logFilePath)
    # allForks = getAllForksOnRepo(repoOwner, repoName)

    # get timestamp representing today at 00:00
    today = datetime.today()
    today = date(today.year, today.month, today.day)
    today = calendar.timegm(today.timetuple())

    # get timestamp representing the furthest day back the data goes at 00:00
    startDate = datetime.strptime(allCommits[-1]["Date"], "%Y-%m-%d").date()
    limit = calendar.timegm(startDate.timetuple())

    d = today
    while d >= limit:
        activity.append({
            "Timestamp": d,
            "Date": datetime.utcfromtimestamp(d).strftime("%Y-%m-%d"),
            "Commits": 0,
            "Additions": 0,
            "Deletions": 0,
            "Changes": 0,
            "Unique authors": [],
            "Number of unique authors": 0,
            "Files changed": [],
            "Number of files changed": 0
        })
        d -= (60 * 60 * 24)

    for commit in allCommits:
        el = next((x for x in activity if x["Date"] == commit["Date"]), None)
        if el != None:
            i = activity.index(el)
            activity[i]["Commits"] += 1
            activity[i]["Additions"] += commit["Additions"]
            activity[i]["Deletions"] += commit["Deletions"]
            activity[i]["Changes"] += commit["Changes"]
            if commit["Author name"] not in activity[i]["Unique authors"]:
                activity[i]["Unique authors"].append(commit["Author name"])
                activity[i]["Number of unique authors"] += 1
            for fn in commit["Files changed"]:
                if fn not in activity[i]["Files changed"]:
                    activity[i]["Files changed"].append(fn)
                    activity[i]["Number of files changed"] += 1

    return activity

def getAllCommitsOnRepo(repoOwner, repoName, logFilePath):
    commits = []
    url = "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/commits"
    headers = {"Authorization": "token %s" % token}
    p = 1

    #check if we're resuming
    if os.path.exists(logFilePath):
        with open(logFilePath) as logFile:
            lines = logFile.read().splitlines()
            lastLine = lines[-1]
            lastLineWords = lastLine.split(" ")
            p = int(lastLineWords[0]) + 1
            url = lastLineWords[-1]
        with open(os.path.join(baseDir, "Data", "GithubData", "NewCommits", repoName+"_commits.json")) as commitFile:
            commits = json.load(commitFile)

    while True:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
    
        data = json.load(response)

        commits += map(parseCommit, data)

        stdout.write("\r%d pages of commits downloaded" % p)
        stdout.flush()

        url = parseLinkHeader(response)
        if url == None:
            break

        if p % 5 == 0:
            with open(os.path.join(baseDir, "Data", "GithubData", "NewCommits", repoName+"_commits.json"), "w+", encoding="utf-8") as dest:
                json.dump(commits, dest, ensure_ascii=False, indent=4)
            with open(logFilePath, "a+") as f:
                f.write("%d pages of commits scraped - next page is at %s\n" % (p, url))

        p += 1

    with open(os.path.join(baseDir, "Data", "GithubData", "NewCommits", repoName+"_commits.json"), "w+", encoding="utf-8") as dest:
        json.dump(commits, dest, ensure_ascii=False, indent=4)
    return commits

def getAllForksOnRepo(repoOwner, repoName):
    forks = []
    url = "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/forks"
    headers = {"Authorization": "token %s" % token}
    p = 1

    while True:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        
        data = json.load(response)
        forks += map(parseFork, data)

        stdout.write("\r%d pages of commits downloaded!" % p)
        stdout.flush()
        p += 1

        url = parseLinkHeader(response)
        if url == None:
            break


    # with open("../Data/GithubData/Forks/" + repoName + "_forks.json", "w+", encoding="utf-8") as dest:
    #     json.dump(forks, dest, ensure_ascii=False, indent=4)
    # json2Csv("../Data/GithubData/Forks/" + repoName + "_forks.json")
    return forks


def parseCommit(commit):
    # time.sleep(0.3)
    url = commit["url"]
    (additions, deletions, files) = getAdditionsDeletionsFiles(url)

    commit = commit["commit"]
    return {
        "Author name": commit["author"]["name"],
        "Author email": commit["author"]["email"],
        "Commit message": commit["message"],
        "Additions": additions,
        "Deletions": deletions,
        "Files changed": files,
        "Changes": additions + deletions,
        "Date": commit["committer"]["date"][:10]
    }

def getAdditionsDeletionsFiles(url):
    headers = {"Authorization": "token %s" % token}
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    data = json.load(response)

    return (data["stats"]["additions"], data["stats"]["deletions"], [f["filename"] for f in data["files"]])

def parseFork(fork):
    return {
        "Forked repo name": fork["full_name"],
        "Date": fork["created_at"][:10]
    }

def parseLinkHeader(response):
    linkHeader = response.info().get("Link")
    
    if linkHeader == None:
        return None

    linkArr = linkHeader.split(",")

    linkDict = {}
    for l in linkArr:
        linkDict[l[-5:-1]] = l.lstrip()[1:-13]

    if "next" in linkDict:
        return linkDict["next"]
    else:
        return None

if __name__ == "__main__":
    main()