import json
from six.moves import urllib
from messari import json2Csv
import sys


def main():
    baseApiUrl = "https://api.crunchbase.com/v3.1/"
    apiKey = "eb8607071e2f2034a085c5082620f959"
    blockchainCategoryId = "1fea62013b7c4c9196ec543f5eded46a"

    # get summaries of all organizations in category "blockchain" from the crunchbase API
    #blockchainOrgsSummaries = getAllOrganizationsInCategory(baseApiUrl, apiKey, blockchainCategoryId)

    # export summaries to JSON file
    #storeOrgsInJson(blockchainOrgsSummaries, "./Data/CrunchbaseData/BlockchainOrganizationsSummary.json")

    # get more detailed data on organizations
    #blockchainOrgsDetails = fetchDetailedInfo("./Data/CrunchbaseData/BlockchainOrganizationsSummary.json", apiKey)

    # export detailed data to JSON file
    #storeOrgsInJson(blockchainOrgsDetails, "./Data/CrunchbaseData/BlockchainOrganizationsDetails.json")
    json2Csv("./Data/CrunchbaseData/BlockchainOrganizationsSummary.json")


def getAllOrganizationsInCategory(baseApiUrl, key, categoryId):
    # initialise array to store all the organizations
    orgs = []

    # get the first page of results from the crunchbase API
    response = urllib.request.urlopen(baseApiUrl + "organizations?user_key=" + key + "&category_uuids=" + categoryId)
    data = json.load(response)
    print(str(data["data"]["paging"]["total_items"]) + " across " + str(data["data"]["paging"]["number_of_pages"]) + " pages")
    print("current page: " + str(data["data"]["paging"]["current_page"]))

    # add the data from the first page of results to the orgs array
    orgs += data["data"]["items"]

    # traverse through the remaining pages of results, adding each page's
    # data to the orgs array
    currentPage = data["data"]["paging"]["current_page"]
    numPages = data["data"]["paging"]["number_of_pages"]

    while currentPage < numPages:
        response = urllib.request.urlopen(data["data"]["paging"]["next_page_url"] + "&user_key=" + key)
        data = json.load(response)

        orgs += data["data"]["items"]

        currentPage = data["data"]["paging"]["current_page"]
        print("current page: " + str(currentPage))
    
    return orgs


def storeOrgsInJson(orgs, outputFile):
    with open(outputFile, "w+", encoding="utf-8") as dest:
        json.dump(orgs, dest, ensure_ascii=False, indent=4)


def fetchDetailedInfo(inputFile, key):
    with open(inputFile) as f:
        summaries = json.load(f)
        for i in range(len(summaries)):

            print("fetching more detailed data: organization " + str(i) + " of " + str(len(summaries)))
            sys.stdout.write("\033[F")

            url = summaries[i]["properties"]["api_url"]
            try:
                response = urllib.request.urlopen(url + "?user_key=" + key)
                resp = json.load(response)
                summaries[i] = resp["data"]
            except:
                pass

    return summaries


if __name__== "__main__":
  main()