import discord
import snscrape.modules.twitter as sntwitter
from discord.ext import tasks

client = discord.Client()

@tasks.loop(minutes=30)
async def scrape_tweets():
    channel = client.get_channel('your channel id here')

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:DOTA2').get_items()):
        if "International" in tweet.content or "ticket" in tweet.content:
            await channel.send("THE INTERNATIONAL 2021 INFO IS OUT")
            await channel.send(tweet.content)
        if i > 3:
            break


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    scrape_tweets.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$scrape'):
        tweets_list = []

        for i, tweet in enumerate(sntwitter.TwitterSearchScraper('from:DOTA2').get_items()):
            if i > 4:
                break
            tweets_list.append(([tweet.date, tweet.id, tweet.content, tweet.user.username]))
        print(len(tweets_list))
        reply = 'These are the last five tweets made by @DOTA2 twitter: \n'
        for tweet in tweets_list:
            print(type(tweet[2]))
            if "International" in tweet[2] or "ticket" in tweet[2]:
                reply = reply + "The next tweet contains information about TI2021 or tickets: \n"
                reply = reply + str(tweet[0]) + " By: " + str(tweet[3]) + " - " + str(tweet[2]) + "\n"
            else:
                reply = reply + str(tweet[0]) + " By: " + str(tweet[3]) + " - " + str(tweet[2]) + "\n"
        await message.channel.send(reply)

client.run('your token here')