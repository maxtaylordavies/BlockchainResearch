from six.moves import urllib
import json
from sys import stdout
from messari import json2Csv

def main():
    token = "15d86cdd72e40499079d533714c3368fb0db77ef"
    getAllCommitsOnRepo("0xProject", "0x-monorepo", token)

def getAllCommitsOnRepo(repoOwner, repoName, token):
    commits = []
    url = "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/commits"
    headers = {"Authorization": "token %s" % token}
    p = 1

    while True:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        linkHeader = response.info().get("Link")

        data = json.load(response)
        commits += map(parseCommit, data)

        stdout.write("\r%d pages of commits downloaded" % p)
        stdout.flush()
        p += 1

        if "next" in linkHeader:
            url = linkHeader.split(";")[0][1:-1]
        else:
            break

    with open("../Data/GithubData/Commits/" + repoName + "_commits.json", "w+", encoding="utf-8") as dest:
        json.dump(commits, dest, ensure_ascii=False, indent=4)
    json2Csv("../Data/GithubData/Commits/" + repoName + "_commits.json")

def parseCommit(commit):
    commit = commit["commit"]
    return {
        "Author name": commit["author"]["name"],
        "Author email": commit["author"]["email"],
        "Commit message": commit["message"],
        "Date": commit["committer"]["date"]
    }

if __name__ == "__main__":
    main()