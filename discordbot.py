import os
import discord
import redis

# param
GET_REACTION_CHANNEL_ID = int(os.environ.get('ENV_GET_REACTION_CH_ID'))
POST_NOTIFIER_CHANNEL_ID = int(os.environ.get('ENV_POST_NOTIFIER_CH_ID'))
MEMBER_ROLE_ID = int(os.environ.get('ENV_MEMBER_ROLE_ID'))
REDIS_URL = os.environ.get('REDIS_URL')
DISCORD_BOT_TOKEN = os.environ.get('ENV_DISCORD_BOT_TOKEN')

r = redis.from_url(REDIS_URL)

# initialize client
client = discord.Client()

@client.event
async def on_ready():
    print('Login.')

@client.event
async def on_message(message):
    if message.channel.id != GET_REACTION_CHANNEL_ID:
        return
    members = message.guild.members
    msg = f'Author: {message.author.name}\n'
    msg += f"Content: {message.content.replace('@', '')}\n"
    msg += '\n'.join([f'> `{m.name}`' for m in [m for m in members if m.name != message.author.name] for r in m.roles if r.id == MEMBER_ROLE_ID])
    bot_message = await client.get_channel(POST_NOTIFIER_CHANNEL_ID).send(msg)
    r.set(message.id, bot_message.id)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id != GET_REACTION_CHANNEL_ID:
        return
    target_msg = await client.get_channel(POST_NOTIFIER_CHANNEL_ID).fetch_message(int(r.get(reaction.message.id)))
    msg = target_msg.content
    new_msg = '\n'.join([f'{m} {reaction.emoji}' if user.name in m else m for m in msg.split('\n')])
    await target_msg.edit(content = new_msg)

client.run(DISCORD_BOT_TOKEN)
