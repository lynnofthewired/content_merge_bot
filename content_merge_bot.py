import discord
import os
import json
from discord.ext import commands
from discord import PermissionOverwrite, Permissions

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='$', intents=intents)

intents.guilds = True
intents.messages = True
intents.message_content = True

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

    async for message in channel1.history(oldest_first=True):
        await new_channel.send(f"**{message.author.name} at {message.created_at} said**:\n{message.content}")

    async for message in channel2.history(oldest_first=True):
        await new_channel.send(f"**{message.author.name} at {message.created_at} said**:\n{message.content}")

with open('config.json') as config_file:
    config = json.load(config_file)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'An error occurred: {str(error)}')

bot.run(config['token'])

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

    for channel in [channel1, channel2]:
        async for message in channel.history(oldest_first=True):
            content = f"{message.author.name} at {message.created_at} said:\n{message.content}"
            files = await process_attachments(message.attachments)
            await new_channel.send(content=content, files=files)

async def process_attachments(attachments):
    files = []
    for attachment in attachments:
        # Download the attachment to a file in memory
        fp = io.BytesIO()
        await attachment.save(fp)
        files.append(discord.File(fp, filename=attachment.filename))
    return files