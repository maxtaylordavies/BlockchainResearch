import json
from six.moves import urllib

def main():
    baseApiUrl = "https://api.crunchbase.com/v3.1/"
    apiKey = "eb8607071e2f2034a085c5082620f959"
    getAllOrganizations(baseApiUrl, apiKey)


def getAllOrganizations(baseApiUrl, key):
    response = urllib.request.urlopen("https://api.crunchbase.com/v3.1/organizations?user_key=eb8607071e2f2034a085c5082620f959")
    data = json.load(response)
    with open("./test.json", "w+") as dest:
        json.dump(data, dest)

if __name__== "__main__":
  main()