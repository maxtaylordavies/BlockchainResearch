from telethon import TelegramClient
import json 
import os
from etherscan import baseDir
from sys import stdout

baseDir += "/Data/OtherChains"
config = {"apiId": 1135644, "apiHash": "059708670710633342ed2f24d8a0e877", "phoneNumber": "+447858288396", "username": "maxtaylordavies"}
client = TelegramClient('anon', config["apiId"], config["apiHash"])

async def main():
    channelNames = {
        # "aeternity": ["aeternity"],
        "bnb": ["binance_announcements"],
        "bytom": ["BytomInternational"],
        "cardano": ["CardanoAnnouncements"],
        "dash": ["dash_chat", "dashnewsbot"],
        "digibyte": ["DigiByteCoin", "DGBalerts", "DigiByteDevelopers"],
        "icon": ["hello_iconworld"],
        "litecoin": ["litecoin"],
        "monero": ["bitmonero"],
        "nebulas": ["nebulasen"],
        "neo": ["NEO_EN"],
        "pivx": ["PIVXChat"],
        "qtum": ["qtumofficial"],
        "stellar": ["StellarLumens"],
        "tron": ["tronnetworkEN"],
        "vechain": ["vechain_official_english"],
        "verge": ["VERGExvg"],
        "vertcoin": ["VertcoinCrypto"],
        "waves": ["wavesnews"],
        "zilliqa": ["zilliqachat"]
    }
    for chain,names in channelNames.items():
        # create directory to store data if not already exists
        d = os.path.join(baseDir, chain, "Telegram")
        if not os.path.exists(d):
            os.makedirs(d)
        # get the entire chat history of each associated channel and store as JSON
        for name in names:
            stdout.write("\rnow mining channel %s" % name)
            stdout.flush()
            channel = await client.get_entity(name)
            messages = await getAllMessagesFromChannel(channel)
            with open(os.path.join(d, name+".json"), "w+", encoding="utf-8") as dest:
                json.dump(messages, dest, ensure_ascii=False, indent=4)

async def getMinAndMaxIds(channel):
    firstMessage = await client.get_messages(channel, limit=1, reverse=True)
    lastMessage = await client.get_messages(channel, limit=1)
    return (firstMessage[0].id, lastMessage[0].id)

async def getAllMessagesFromChannel(channel):
    (minId, maxId) = await getMinAndMaxIds(channel)

    messages = await client.get_messages(channel, min_id=minId, max_id=maxId)

    print(len(messages))

    messagesJson = list(map(lambda m: {
        "Message Id": m.id,
        "Sender Id": m.from_id,
        "Post": m.post,
        "Date": m.date.strftime("%d-%m-%Y %H:%M:%S"),
        "Body": m.message,
        "Parent message id": m.reply_to_msg_id,
        "Views": m.id,
        "Post author": m.post_author
    }, messages))

    return messagesJson
    
with client:
    client.loop.run_until_complete(main())

