import json
import csv
import os
from misc.messari import json2Csv
from six.moves import urllib

baseDir = os.getenv("HOME") + "/Dropbox/SHARED BLOCKCHAIN PROJECT - DATA/Max Taylor-Davies"
baseDir = os.path.join(baseDir, "Data", "coinmetrics-messari-summary", "messari", "timeseries")

def getContributorData():
    with open("./messari-assets-contributors.json") as f:
        data = json.load(f)
        data = data["data"]

    assets = [a for a in data if a["profile"]["people"]["contributors"] != None]
    people = [dict([("Coin", a["symbol"])] + list(p.items())) for a in assets for p in a["profile"]["people"]["contributors"]]

    with open("./messari-contributor-data.csv", "w+") as dest:
        w = csv.DictWriter(dest, people[0].keys())
        w.writeheader()
        w.writerows(people)

def getTimeSeriesData(assetId, metricId):
    series = []  
    for year in range(10, 21):
        url = "https://data.messari.io/api/v1/assets/%s/metrics/%s/time-series?interval=1d&timestamp-format=rfc3339&order=ascending&start=20%s-01-01&end=20%s-01-01" % (assetId, metricId, str(year), str(year+1))
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = json.load(response)
        data = data["data"]

        schema = data["schema"]["values_schema"]

        if data["values"] == None:
            continue

        series += data["values"]
    return [series, schema]


def main():
    assets = [
        {"Name":"Bitcoin", "id":"1e31218a-e44e-4285-820c-8282ee222035"},
        {"Name":"Ethereum", "id":"21c795f5-1bfd-40c3-858e-e9d7e820c6d0"},
        {"Name":"Tether", "id":"51f8ea5e-f426-4f40-939a-db7e05495374"},
        {"Name":"XRP", "id":"97775be0-2608-4720-b7af-f85b24c7eb2d"},
        {"Name":"Bitcoin Cash", "id":"c8c7e9a1-844d-4cfd-9dbc-ce85a8a9613f"},
        {"Name":"Bitcoin SV", "id":"ecef109b-64d3-4f3d-9789-e901ef7bacfb"},
        {"Name":"Litecoin", "id":"c7c3697d-1b9c-42bf-9664-a366634ce2b3"},
        {"Name":"BNB", "id":"7dc551ba-cfed-4437-a027-386044415e3e"},
        {"Name":"EOS", "id":"2e9a4c5d-7966-47c4-aebd-cdbc1ecf9d2e"},
        {"Name":"Tezos", "id":"6d667f96-24f2-420b-9a22-73f5cd594bcf"},
        {"Name":"Chainlink", "id":"a9c04b71-33e4-4fed-8126-cf1612c7e198"},
        {"Name":"LEO", "id":"28681c70-d3a1-4139-942e-c4bdcc49ad64"},
        {"Name":"Cardano", "id":"362f0140-ecdd-4205-b8a0-36f0fd5d8167"},
        {"Name":"Monero", "id":"cd738ecc-ef84-47b5-be73-d064eff3e36e"},
        {"Name":"TRON", "id":"1c077d6e-99c7-491c-b24d-1d359011cd81"},
        {"Name":"Huobi Token", "id":"2c0fc0e2-def8-4666-b542-c68378230551"},
        {"Name":"Stellar", "id":"7c435a77-5be9-4424-b5d1-1c02b968c56f"},
        {"Name":"Dash", "id":"e6702473-8eb4-4188-ba5b-338bf8b2398f"},
        {"Name":"USD Coin", "id":"4515ba15-2719-4183-b0ca-b9255d55b67e"},
        {"Name":"Crypto.com Chain", "id":"de533c50-6a57-4975-bb83-62862fb9af09"}
    ]
    metricIds = ["sply.circ", "mcap.circ", "price"]
    
    for asset in assets[13:]:
        assetName = asset["Name"]
        assetId = asset["id"]
        for metric in metricIds:
            [data, schema] = getTimeSeriesData(assetId, metric)

            if not os.path.exists(os.path.join(baseDir, assetName)): 
                os.mkdir(os.path.join(baseDir, assetName))

            with open(os.path.join(baseDir, assetName, metric.replace(".","-")+".csv"), "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(list(schema.keys()))
                writer.writerows(data)


    

if __name__ == "__main__":
    main()