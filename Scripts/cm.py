import json
import csv

def main():
    thisara_vars = [
        "AdrActCnt",
        "CapMrktCurUSD",
        "NVTAdj",
        "NVTAdj90",
        "PriceBTC",
        "PriceUSD",
        "ROI1yr",
        "ROI30d",
        "SplyCur",
        "TxCnt",
        "TxTfr",
        "TxTfrValAdjNtv",
        "TxTfrValAdjUSD",
        "TxTfrValMeanNtv",
        "TxTfrValMeanUSD",
        "TxTfrValMedNtv",
        "TxTfrValMedUSD",
        "TxTfrValNtv",
        "TxTfrValUSD",
        "VtyDayRet180d",
        "VtyDayRet30d",
        "VtyDayRet60d"
    ]

    with open("./cm-variables.json") as f:
        all_vars = json.load(f)
    all_vars = [{"Variable name": v["id"], "Description": v["description"], "Present in Thisara's data": thisaraHasMetric(v["id"], thisara_vars)} for v in all_vars["metricsInfo"]]

    with open("./cm-all-vars.csv", "w+") as dest:
        w = csv.DictWriter(dest, all_vars[0].keys())
        w.writeheader()
        w.writerows(all_vars)    
    
    # # new_vars = [v for v in all_vars if v["Variable name"] not in thisara_vars]

    # # with open("./cm-new-vars.csv", "w+") as dest:
    # #     w = csv.DictWriter(dest, new_vars[0].keys())
    # #     w.writeheader()
    # #     w.writerows(new_vars)

    # allMetricIds = [v["Variable name"] for v in all_vars]
    # assets_metrics = []
    # with open("./cm-assets-metrics.json") as f:
    #     data = json.load(f)
    #     data = data["assetsInfo"]  

    # for asset in data:
    #     d1 = {"Asset id": asset["id"], "Asset name": asset["name"]}
    #     d2 = {metric: assetHasMetric(asset, metric) for metric in allMetricIds}
    #     d = dict(list(d1.items()) + list(d2.items()))
    #     assets_metrics.append(d) 

    # with open("./cm-assets-metrics.csv", "w+") as dest:
    #     w = csv.DictWriter(dest, assets_metrics[0].keys())
    #     w.writeheader()
    #     w.writerows(assets_metrics)
    

def assetHasMetric(asset, metric):
    return "yes" if metric in asset["metrics"] else "no"

def thisaraHasMetric(metric, thisara):
    return "yes" if metric in thisara else "no"

if __name__ == "__main__":
    main()