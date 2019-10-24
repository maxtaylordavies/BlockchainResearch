from pycoingecko import CoinGeckoAPI
from messari import json2Csv
import json
import time


def main():
    # initialise an instance of the API client
    api = CoinGeckoAPI()

    # load a list containing the symbols of all the coins we're interested in
    symbols = getDesiredCoinSymbols()

    # find the ids of the coins we're interested in
    allCoins = api.get_coins_list()
    ids = getDesiredCoinIds(allCoins, symbols)
    
    # get historical data on coins by id
    for id in ids:
        getHistoricalDataOnCoin(api, id)


def getHistoricalDataOnCoin(api, id):
    data = []
    hist = api.get_coin_market_chart_by_id(id=id, vs_currency="usd", days="max")

    prices = list(map(lambda x: x[1], hist["prices"]))
    marketCaps = list(map(lambda x: x[1], hist["market_caps"]))
    totalVolumes = list(map(lambda x: x[1], hist["total_volumes"]))
    timestamps = list(map(lambda x: x[0], hist["prices"]))

    for i in range(len(timestamps)):
        data.append({
            "Date": time.strftime("%d-%m-%Y", time.localtime(timestamps[i]/1000)),
            "Price (USD)": prices[i],
            "Market cap": marketCaps[i],
            "Total volume": totalVolumes[i]
        })

    jsonPath = "../Data/CoingeckoData/JSON/"+id+".json"
    csvPath = "../Data/CoingeckoData/CSV/"+id+".csv"

    with open(jsonPath, "w+", encoding="utf-8") as dest:
        json.dump(data, dest, ensure_ascii=False, indent=4)

    json2Csv(jsonPath, csvPath=csvPath)    


def getDesiredCoinIds(coins, symbols):
    return [c["id"] for c in list(filter(lambda x: x["symbol"] in symbols, coins))]


def getDesiredCoinSymbols():
    return [
        "ada",
        "ae",
        "aion",
        "ant",
        "bat",
        "bch",
        "bnb",
        "bsv",
        "btc",
        "btg",
        "btm",
        "cvc",
        "dai",
        "dash",
        "dcr",
        "dgb",
        "doge",
        "drgn",
        "elf",
        "eng",
        "eos",
        "etc",
        "eth",
        "ethos",
        "fun",
        "gas",
        "gno",
        "gnt",
        "grin",
        "gusd",
        "icx",
        "kcs",
        "knc",
        "loom",
        "lrc",
        "lsk",
        "ltc",
        "maid",
        "mana",
        "mkr",
        "nas",
        "neo",
        "omg",
        "pax",
        "pay",
        "pivx",
        "poly",
        "powr",
        "ppt",
        "qash",
        "qtum",
        "rep",
        "snt",
        "trx",
        "tusd",
        "usdc",
        "usdt",
        "vet",
        "vtc",
        "waves",
        "wtc",
        "xem",
        "xlm",
        "xmr",
        "xrp",
        "xtz",
        "xvg",
        "zec",
        "zil",
        "zrx"
    ]

if __name__== "__main__":
  main()