import json
from six.moves import urllib
from pandas.io.json import json_normalize   

def main():
    # get asset data
    getJsonData("https://data.messari.io/api/v1/assets", "./MessariData/AssetData.json")
    json2Csv("./MessariData/AssetData.json", "data")

def getJsonData(url, outputFile):
    response = urllib.request.urlopen(url)
    data = json.load(response)
    with open(outputFile, "w+", encoding="utf-8") as dest:
        json.dump(data, dest, ensure_ascii=False, indent=4)

def json2Csv(jsonFile, key=None):
    # open json file
    with open(jsonFile) as data:    
        data = json.load(data)

    # flatten structured json data
    df = json_normalize(data, key)

    # export to csv file
    csvPath = jsonFile[:-4] + "csv"
    df.to_csv(csvPath)

if __name__== "__main__":
  main()