import discord
import asyncio

async def fetchAllMessagesInChannel(channel):
    messages = await channel.history(limit=10000).flatten()
    print(len(messages))
    
        

async def main():
    # baseApiUrl = "https://discordapp.com/api"
    client = discord.Client()
    token = "NjQyNDAwNDM0NDcxODI5NTMy.Xk05Gw.BIXv69aAY14GqrUY9s6KBnobHX8"
    await client.login(token, bot=False)

    guilds = await client.fetch_guilds(limit=150).flatten()
    # print(guilds[1].get_channel("389607108926111746"))
    channels = await guilds[1].fetch_channels()
    for c in channels:
        if c.id == 389607108926111746:
            announcements = c

    await fetchAllMessagesInChannel(announcements)

    await client.logout()


if __name__ == "__main__":
   loop = asyncio.get_event_loop()
   loop.run_until_complete(main())