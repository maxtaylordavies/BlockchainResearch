from six.moves import urllib
import json
import time
from datetime import datetime, date
import calendar
from misc.messari import json2Csv

def main():
    submissions = getAllSubmissionsFromSubreddit("Tether")
    stats = getSubmissionNumbersForSubreddit("Tether")
    with open("test.json", "w+", encoding="utf-8") as dest:
        json.dump(submissions, dest, ensure_ascii=False, indent=4)
    with open("test2.json", "w+", encoding="utf-8") as dest:
        json.dump(stats, dest, ensure_ascii=False, indent=4)

def getSubmissionNumbersForSubreddit(subreddit):
    submissions = getAllSubmissionsFromSubreddit(subreddit)
    submissionNumbers = []

    today = datetime.today()
    today = date(today.year, today.month, today.day)
    today = calendar.timegm(today.timetuple())

    limit = submissions[-1]["created_utc"] - (60 * 60 * 24)
    d = today

    while d >= limit:
        submissionNumbers.append({
            "Timestamp": d,
            "Date": datetime.utcfromtimestamp(d).strftime("%Y-%m-%d"),
            "Submissions": 0
        })
        d -= (60 * 60 * 24)

    for submission in submissions:
        dayCreated = startOfDay(submission["created_utc"])
        el = next((x for x in submissionNumbers if x["Timestamp"] == dayCreated), None)
        if el != None:
            i = submissionNumbers.index(el)
            submissionNumbers[i]["Submissions"] += 1

    return submissionNumbers

def getAllSubmissionsFromSubreddit(subreddit):
    submissions = []
    url = "https://api.pushshift.io/reddit/search/submission?subreddit=" + subreddit + "&fields=created_utc,title,author&size=500"
    beforeTime = round(time.time())
    limit = 1483228800 # Jan 1 2017 00:00:00
    #limit = 1569931372

    while beforeTime > limit:
        response = urllib.request.urlopen(url + "&before=" + str(beforeTime))
        data = json.load(response)["data"]

        if len(data) == 0:
            break

        newBeforeTime = data[len(data)-1]["created_utc"]
        # if (beforeTime - newBeforeTime) > 600000:
        #     print(datetime.utcfromtimestamp(newBeforeTime).strftime("%Y-%m-%d"))
        
        beforeTime = newBeforeTime
        submissions += data

    return submissions

def getAllCommentsFromSubreddit(subreddit):
    return 0

def startOfDay(ts):
    d = datetime.utcfromtimestamp(ts)
    return calendar.timegm(date(d.year,d.month,d.day).timetuple())

if __name__ == "__main__":
    main()