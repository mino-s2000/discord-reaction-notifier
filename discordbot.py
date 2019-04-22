import os
import discord
from pytz import timezone
from datetime import datetime

# param
<<<<<<< HEAD
getReactionChId = os.environ.get('ENV_GET_REACTION_CH_ID') # Channel ID to post the message you want to get a reaction from.
postNotifierChId = os.environ.get('ENV_POST_NOTIFIER_CH_ID') # Channel ID posted by this BOT.
=======
cAnnounceId = 531286859611897858 # Channel ID to post the message you want to get a reaction from.
cAnnounceBotId = 567747363276455980 # Channel ID posted by this BOT.
>>>>>>> 22bd141c79dd33d7f773a7ef9e06446b75125e9d

# initialize client
client = discord.Client()

@client.event
async def on_ready():
    print('Login.')

@client.event
async def on_reaction_add(reaction, user):
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

<<<<<<< HEAD
client.run(os.environ.get('ENV_DISCORD_BOT_TOKEN'))
=======
client.run('NTY3NzQ0NjY4NTExNjMzNDA4.XLX_gw.tkdFmlqoBKzHVAfTi0rQ4pengL0')
>>>>>>> 22bd141c79dd33d7f773a7ef9e06446b75125e9d
