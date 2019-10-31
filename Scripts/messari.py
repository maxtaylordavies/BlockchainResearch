import json
from six.moves import urllib
from pandas.io.json import json_normalize   

def main():
    # get asset data
    getJsonData("https://data.messari.io/api/v1/assets", "./Data/MessariData/AssetData.json")
    json2Csv("../Data/MessariData/AssetData.json", "data")

def getJsonData(url, outputFile):
    response = urllib.request.urlopen(url)
    data = json.load(response)
    with open(outputFile, "w+", encoding="utf-8") as dest:
        json.dump(data, dest, ensure_ascii=False, indent=4)

def json2Csv(jsonFile, key=None, csvPath=None):
    # open json file
    with open(jsonFile) as data:    
        data = json.load(data)

    # flatten structured json data
    df = json_normalize(data, key)

    # export to csv file
    if csvPath == None:
        csvPath = jsonFile[:-4] + "csv"
    df.to_csv(csvPath)

if __name__ == "__main__":
  main()