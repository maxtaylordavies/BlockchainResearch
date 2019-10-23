from pycoingecko import CoinGeckoAPI

def main():
    # initialise an instance of the API client
    api = CoinGeckoAPI()

    # load a list containing the symbols of all the coins we're interested in
    symbols = getDesiredCoinSymbols()

    # find the ids of the coins we're interested in
    allCoins = api.get_coins_list()
    ids = getDesiredCoinIds(allCoins, symbols)
    print(ids)
    

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