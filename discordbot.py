import os
import discord
from pytz import timezone
from datetime import datetime

# initialize client
client = discord.Client()

@client.event
async def on_ready():
    print('Login.')

@client.event
async def on_reaction_add(reaction, user):
    # param
    getReactionChId = int(os.environ.get('ENV_GET_REACTION_CH_ID')) # Channel ID to post the message you want to get a reaction from.
    postNotifierChId = int(os.environ.get('ENV_POST_NOTIFIER_CH_ID')) # Channel ID posted by this BOT.

    if reaction.message.channel.id != getReactionChId:
        return
    cAnnounceBot = client.get_channel(postNotifierChId)
    # Get the datetime when the message was posted.
    # 'reaction.message.created_at' is UTC. But not set timezone data.
    mDatetime = timezone('UTC').localize(reaction.message.created_at)
    # Localize 'reaction.message.created_at'.
    mDatetime = mDatetime.astimezone(timezone('Asia/Tokyo')).strftime('%Y-%m-%d %X')
    reply = f'{user} is reacted. Target Message Posted At: {mDatetime}'
    await cAnnounceBot.send(reply)

client.run(os.environ.get('ENV_DISCORD_BOT_TOKEN'))
