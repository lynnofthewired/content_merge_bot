import discord
import os
import json
import io
from discord.ext import commands
from discord import PermissionOverwrite, Permissions

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def merge(ctx, channel1: discord.TextChannel, channel2: discord.TextChannel):
    overwrites = {
        ctx.guild.default_role: PermissionOverwrite(read_messages=False),
        ctx.author: PermissionOverwrite(read_messages=True),
        bot.user: PermissionOverwrite(read_messages=True)
    }

    new_channel = await ctx.guild.create_text_channel(
        f'merged-{channel1.name}-{channel2.name}', 
        overwrites=overwrites
    )

    messages = []
    for channel in [channel1, channel2]:
        async for message in channel.history(oldest_first=True):
            content = f"{message.author.name} at {message.created_at} said:\n{message.content}"
            files = await process_attachments(message.attachments)
            messages.append((message.created_at.timestamp(), content, files))

    messages.sort()  # Sort messages by timestamp

    for _, content, files in messages:
        await new_channel.send(content=content, files=files if files else None)

async def process_attachments(attachments):
    files = []
    for attachment in attachments:
        fp = io.BytesIO()
        await attachment.save(fp)
        files.append(discord.File(fp, filename=attachment.filename))
    return files

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'An error occurred: {str(error)}')

with open('config.json') as config_file:
    config = json.load(config_file)

bot.run(config['token'])


# intermediary step where we create a new dictionary where each post has a Unix timestamp

# It's cool to vent and stuff, but be aware of your own privacy needs in this growing server 
# Don't be here looking for partners

# General

# Events --> Events becomes a category. Different channels for different types of events Beach night, Shows/clubs, Games/Magic?? , Tonight, Planning, Parties/get-togethers/high tea