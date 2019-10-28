from pytrends.request import TrendReq
import time

def main():
    pytrends = TrendReq(hl='en-US', tz=0)

    searchTerms = getSearchTerms()
    for term in searchTerms:
        getStatsForSearchTerm(pytrends, term)
        # rate limiting
        time.sleep(1)

def getStatsForSearchTerm(client, term):
    client.build_payload(kw_list=[term])
    df = client.interest_over_time()

    try:
        df = df.drop(columns=["isPartial"])
    except:
        pass

    df.rename(columns={term:"search interest"}, inplace=True)
    df.to_csv("../Data/GoogleTrendsData/" + term + ".csv")

def getSearchTerms():
    return [
        '0x', 
        'aelf', 
        'Aeternity', 
        'Aion', 
        'Aragon', 
        'Augur', 
        'Basic Attention Token', 
        'Batcoin', 
        'Binance Coin', 
        'Bitcoin', 
        'Bitcoin Cash', 
        'Bitcoin SV', 
        'Bitcoin Gold', 
        'Bytom', 
        'Calvarycoin', 
        'Cardano', 
        'Civic', 
        'Dai', 
        'Dash', 
        'Decentraland', 
        'Decred', 
        'DigiByte', 
        'Dogecoin', 
        'Dragonchain', 
        'Enigma', 
        'EOS', 
        'Ethereum', 
        'Ethereum Classic', 
        'Ethos', 
        'FunFair', 
        'Gas', 
        'Gemini Dollar', 
        'Gnosis', 
        'Golem', 
        'Grin', 
        'ICON', 
        'KuCoin Shares', 
        'Kyber Network', 
        'Lisk', 
        'Litecoin', 
        'Loom Network', 
        'Loopring', 
        'MaidSafeCoin', 
        'Maker', 
        'Monero', 
        'Nebulas', 
        'NEM', 
        'NEO', 
        'OmiseGO', 
        'Paxos Standard', 
        'Pay Chain', 
        'PIVX', 
        'Polymath Network', 
        'Populous', 
        'Power Ledger', 
        'QASH', 
        'Qtum', 
        'XRP', 
        'Stellar', 
        'TenX', 
        'Tether', 
        'Tezos', 
        'TRON', 
        'TronFun Token', 
        'TrueUSD', 
        'USD Coin', 
        'VeChain', 
        'Verge', 
        'Vertcoin', 
        'Vote Coin', 
        'Waltonchain', 
        'Waves', 
        'Zcash', 
        'Zilliqa'
    ]

if __name__== "__main__":
  main()