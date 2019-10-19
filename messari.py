import json
from six.moves import urllib
from pandas.io.json import json_normalize   

def main():
    # get asset data
    getJsonData("https://data.messari.io/api/v1/assets", "./MessariData/AssetData.json")
    json2Csv("./MessariData/AssetData.json")

def getJsonData(url, outputFile):
    response = urllib.request.urlopen(url)
    data = json.load(response)
    with open(outputFile, "w+") as dest:
        json.dump(data, dest)

def json2Csv(jsonFile):
    # open json file
    with open(jsonFile) as data:    
        data = json.load(data)

    # flatten structured json data
    df = json_normalize(data, "data")

    # export to csv file
    csvPath = jsonFile[:-4] + "csv"
    df.to_csv(csvPath)

if __name__== "__main__":
  main()