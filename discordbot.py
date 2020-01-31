import os
import discord
import redis
from datetime import datetime

# param
GET_REACTION_CHANNEL_ID = int(os.environ.get('ENV_GET_REACTION_CH_ID'))
POST_NOTIFIER_CHANNEL_ID = int(os.environ.get('ENV_POST_NOTIFIER_CH_ID'))
MEMBER_ROLE_ID = int(os.environ.get('ENV_MEMBER_ROLE_ID'))
REDIS_URL = os.environ.get('REDIS_URL')
DISCORD_BOT_TOKEN = os.environ.get('ENV_DISCORD_BOT_TOKEN')

# use debug param
#GET_REACTION_CHANNEL_ID = 651742879315656714
#POST_NOTIFIER_CHANNEL_ID = 651742929135599617
#MEMBER_ROLE_ID = 631489002704207872
#REDIS_URL = ''
#DISCORD_BOT_TOKEN = ''

EMBED_COLOR = 0x7fffd4

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
    title = 'お知らせを読んだ方／読んでない方'
#    description = discord.utils.escape_mentions(message.content)
    embed = discord.Embed(
        title = title,
        description = f'お知らせ発信者: {message.author.name}',
        color = EMBED_COLOR,
        timestamp = datetime.utcnow()
    )
    embed.set_footer(text = f"Latest Edit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, User: Bot")
    embed.add_field(
        name = '読んでない方',
        value = '\n'.join([m.name for m in [m for m in members if m.name != message.author.name] for r in m.roles if r.id == MEMBER_ROLE_ID]),
        inline = True
    )
    embed.add_field(
        name = '読んだ方',
        value = '',
        inline = True
    )
    embed_message = await message.channel.send(embed = embed)
    r.set(embed_message.id, bot_message.id)

@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != GET_REACTION_CHANNEL_ID:
        return
    channel = client.get_channel(payload.channel_id)
    target_msg = channel.fetch_message(int(r.get(payload.message_id)))
    msg_embed = target_msg.embeds[0]
    user = client.get_user(payload.user_id)
    unread_field = msg_embed.fields[0]
    read_field = msg_embed.fields[1]

    unread_users = unread_field.value.split('\n')
    if (user.name not in unread_users):
        return
    unread_users = '\n'.join([u for u in unread_users if user.name != u])

    read_users = '\n'.join([read_field.value.split('\n'), user.name])

    msg_embed.set_field_at(index = 0, name = unread_field.name, value = unread_users, inline = True)
    msg_embed.set_field_at(index = 1, name = read_field.name, value = read_users, inline = True)
    msg_embed.set_footer(text = f"Latest Edit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, User: {user.name}")
    await target_msg.edit(embed = msg_embed)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id != GET_REACTION_CHANNEL_ID:
        return
    target_msg = await client.get_channel(POST_NOTIFIER_CHANNEL_ID).fetch_message(int(r.get(reaction.message.id)))
    msg_embed = target_msg.embeds[0]
    new_embed = discord.Embed(
        title = msg_embed.title,
        description = msg_embed.description,
        color = EMBED_COLOR,
        timestamp = msg_embed.timestamp
    )
    new_embed.set_footer(text = f"Latest Edit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, User: {user.name}")
    new_embed.add_field(
        name = 'クラメン一覧',
        value = '\n'.join([f'{m} {reaction.emoji}' if user.name in m else m for m in msg_embed.fields[0].value.split('\n')])
    )
    await target_msg.edit(embed = new_embed)

@client.event
async def on_reaction_remove(reaction, user):
    if reaction.message.channel.id != GET_REACTION_CHANNEL_ID:
        return
    target_msg = await client.get_channel(POST_NOTIFIER_CHANNEL_ID).fetch_message(int(r.get(reaction.message.id)))
    msg_embed = target_msg.embeds[0]
    new_embed = discord.Embed(
        title = msg_embed.title,
        description = msg_embed.description,
        color = EMBED_COLOR,
        timestamp = msg_embed.timestamp
    )
    new_embed.set_footer(text = f"Latest Edit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, User: {user.name}")
    new_embed.add_field(
        name = 'クラメン一覧',
        value = '\n'.join([f'{m.replace(f" {reaction.emoji}", "")}' if user.name in m else m for m in msg_embed.fields[0].value.split('\n')])
    )
    await target_msg.edit(embed = new_embed)

client.run(DISCORD_BOT_TOKEN)
