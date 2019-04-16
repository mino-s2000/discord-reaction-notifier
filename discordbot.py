import discord
from pytz import timezone
from datetime import datetime

# param
cAnnounceId = 000000000000000000 # Channel ID to post the message you want to get a reaction from.
cAnnounceBotId = 111111111111111111 # Channel ID posted by this BOT.

# initialize client
client = discord.Client()

@client.event
async def on_ready():
    print('Login.')

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id != cAnnounceId:
        return
    cAnnounceBot = client.get_channel(cAnnounceBotId)
    # Get the datetime when the message was posted.
    # 'reaction.message.created_at' is UTC. But not set timezone data.
    mDatetime = timezone('UTC').localize(reaction.message.created_at)
    # Localize 'reaction.message.created_at'.
    mDatetime = mDatetime.astimezone(timezone('Asia/Tokyo')).strftime('%Y-%m-%d %X')
    reply = f'{user} is reacted. Target Message Posted At: {mDatetime}'
    await cAnnounceBot.send(reply)

client.run('token')
