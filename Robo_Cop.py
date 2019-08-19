import discord
from discord.ext import commands
import json

# Get the settings file
def getSettingsFile():
    with open("settings.json", "r") as settings_file:
        data = json.load(settings_file)
    return data
settings = getSettingsFile()

# Create the client
client = discord.Client()

# Discord functions
@client.event
async def on_message(message):
    # This removes banned emojis
    for bannedEmoji in settings["bannedEmojis"]:
        if message.content.find(":"+bannedEmoji+":") != -1 and message.author.id != settings["allowed_user_for_emojis"]:
            await message.delete()

    # This is a very specific filter I made for stopping a user from mentioning multiple words in the same message
    if message.author.id == 378666988412731404:
        content = message.content.lower()
        if content.find("hroi") != -1 and (content.find("rickity") != -1 or content.find("rickety") != -1):
            await message.channel.send(message.author.mention+" Please don't mention that fanfic again, it has gone too far.")
            await message.delete()

@client.event
async def on_raw_reaction_add(payload):
    for bannedEmoji in settings["bannedEmojis"]:
        if payload.emoji.name == bannedEmoji and payload.user_id != settings["allowed_user_for_emojis"]:
            guild = client.get_guild(payload.guild_id)

            channel = guild.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

            member = guild.get_member(payload.user_id)

            await message.remove_reaction(payload.emoji, member)

    for reactionRole in settings["reactionRoles"]:
        if payload.message_id == reactionRole["message_id"]:

            guild = client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = guild.get_role(reactionRole["role_id"])
            
            await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    for reactionRole in settings["reactionRoles"]:
        if payload.message_id == reactionRole["message_id"]:
            
            guild = client.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            role = guild.get_role(reactionRole["role_id"])
            
            await member.remove_roles(role)

# Run the Discord but
client.run(settings["Discord_token"])