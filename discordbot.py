import os
import json
import discord

# param
getReactionChId = int(os.environ.get('ENV_GET_REACTION_CH_ID')) # Channel ID to post the message you want to get a reaction from.
postNotifierChId = int(os.environ.get('ENV_POST_NOTIFIER_CH_ID')) # Channel ID posted by this BOT.
memberRoleId = int(os.environ.get('ENV_MEMBER_ROLE_ID')) # Role ID by Guild Member

# initialize client
client = discord.Client()

@client.event
async def on_ready():
    print('Login.')

@client.event
async def on_message(message):
    if message.channel.id != getReactionChId:
        return
    members = message.guild.members
    msg = f'Author: {message.author.name}\n'
    msg += f'Content: {message.content}\n'
    reply = ''
    for member in members:
        if member.name == message.author.name:
            continue
        for role in member.roles:
            if role.id == memberRoleId:
                reply += f'> `{member.name}`\n'
    reply = f'{msg}{reply}'
    bot_message = await client.get_channel(postNotifierChId).send(reply)
    json_data = {}
    with open('message-matching.json', 'r') as fr:
        json_data = json.load(fr)
    json_data['message_matching'].append({"announce_id": message.id, "summary_id": bot_message.id})
    with open('message-matching.json', 'w') as fw:
        json.dump(json_data, fw, indent = 2)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id != getReactionChId:
        return
    json_data = {}
    with open('message-matching.json', 'r') as f:
        json_data = json.load(f)
    summary_ids = [x['summary_id'] for x in json_data['message_matching'] if 'announce_id' in x and 'summary_id' in x and x['announce_id'] == reaction.message.id]
    target_msg = await client.get_channel(postNotifierChId).fetch_message(summary_ids[0])
    msg = target_msg.content
    new_msg = ''
    for m in msg.split('\n'):
        tmp = m
        if m == f'> `{user.name}`':
            tmp = f'> `{user.name}` {reaction.emoji}'
        new_msg += f'{tmp}\n'
    await target_msg.edit(content = new_msg)

client.run(os.environ.get('ENV_DISCORD_BOT_TOKEN'))
