from six.moves import urllib
import json
from sys import stdout
from messari import json2Csv
from datetime import datetime, date
import calendar

def main():
    token = "5d35f0fb65306312a00d45bf68b9770d166bba95"
    getHistoricalActivityOnRepo("0xProject", "0x-monorepo", token)

def getHistoricalActivityOnRepo(repoOwner, repoName, token):
    activity = []
    allCommits = getAllCommitsOnRepo(repoOwner, repoName, token)
    allForks = getAllForksOnRepo(repoOwner, repoName, token)

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
            "Forks": 0
        })
        d -= (60 * 60 * 24)

    for commit in allCommits:
        el = next((x for x in activity if x["Date"] == commit["Date"]), None)
        if el != None:
            i = activity.index(el)
            activity[i]["Commits"] += 1

    for fork in allForks:
        el = next((x for x in activity if x["Date"] == fork["Date"]), None)
        if el != None:
            i = activity.index(el)
            activity[i]["Forks"] += 1

    with open("../Data/GithubData/Activity/" + repoName + "_activity.json", "w+", encoding="utf-8") as dest:
        json.dump(activity, dest, ensure_ascii=False, indent=4)

def getAllCommitsOnRepo(repoOwner, repoName, token):
    commits = []
    url = "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/commits"
    headers = {"Authorization": "token %s" % token}
    p = 1

    while True:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
    
        data = json.load(response)
        commits += map(parseCommit, data)

        stdout.write("\r%d pages of commits downloaded" % p)
        stdout.flush()
        p += 1

        url = parseLinkHeader(response)
        if url == None:
            break

    with open("../Data/GithubData/Commits/" + repoName + "_commits.json", "w+", encoding="utf-8") as dest:
        json.dump(commits, dest, ensure_ascii=False, indent=4)
    # json2Csv("../Data/GithubData/Commits/" + repoName + "_commits.json")
    return commits

def getAllForksOnRepo(repoOwner, repoName, token):
    forks = []
    url = "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/forks"
    headers = {"Authorization": "token %s" % token}
    p = 1

    while True:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        
        data = json.load(response)
        forks += map(parseFork, data)

        stdout.write("\r%d pages of forks downloaded" % p)
        stdout.flush()
        p += 1

        url = parseLinkHeader(response)
        if url == None:
            break

    with open("../Data/GithubData/Forks/" + repoName + "_forks.json", "w+", encoding="utf-8") as dest:
        json.dump(forks, dest, ensure_ascii=False, indent=4)
    # json2Csv("../Data/GithubData/Forks/" + repoName + "_forks.json")
    return forks


def parseCommit(commit):
    commit = commit["commit"]
    return {
        "Author name": commit["author"]["name"],
        "Author email": commit["author"]["email"],
        "Commit message": commit["message"],
        "Date": commit["committer"]["date"][:10]
    }

def parseFork(fork):
    return {
        "Forked repo name": fork["full_name"],
        "Date": fork["created_at"][:10]
    }

def parseLinkHeader(response):
    linkHeader = response.info().get("Link")
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