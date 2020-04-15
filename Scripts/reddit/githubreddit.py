from sys import stdout, path
path.append("..")
path.append("../github-difficulty-addresses")

from github import getHistoricalActivityOnRepo
from reddit import getSubmissionNumbersForSubreddit
from misc.messari import json2Csv
from config.config_file import baseDir, githubToken as apiKey
import json
import os

def main():
    with open(baseDir + "/Scripts/ids.json") as tokens:    
        tokens = json.load(tokens)

    for i in range(12, 50):
        token = tokens[i]
        folder = baseDir + "/Data/TokenData/" + token["name"]
        os.mkdir(folder)

        if token["subreddit"] != "":
            redditStats = getSubmissionNumbersForSubreddit(token["subreddit"])
            with open(folder + "/reddit.json", "w+", encoding="utf-8") as dest:
                json.dump(redditStats, dest, ensure_ascii=False, indent=4)
            json2Csv(folder + "/reddit.json")

        if token["repo"] != "":
            [repoOwner, repoName] = token["repo"].split("/")
            githubStats = getHistoricalActivityOnRepo(repoOwner, repoName, apiKey)
            with open(folder + "/github.json", "w+", encoding="utf-8") as dest:
                json.dump(githubStats, dest, ensure_ascii=False, indent=4)
            json2Csv(folder + "/github.json")

        stdout.write("\rgot stats on" + str(i+1) + "tokens")
        stdout.flush()

if __name__== "__main__":
  main()