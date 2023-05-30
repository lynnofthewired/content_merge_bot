import discord
import os
import json
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

with open('config.json') as config_file:
    config = json.load(config_file)

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def merge(ctx, channel1: discord.TextChannel, channel2: discord.TextChannel):
    # This function is a command for the bot that will merge the contents of two channels into a new one

    # The command takes three arguments:
    # - ctx: The context in which the command was called. This contains information like the message that called the command and the server (guild) in which it was called
    # - channel1 and channel2: These are the two channels that you want to merge. They are of type discord.TextChannel, which means the command expects them to be text channels.

    # First, the bot creates a new channel in the same server (guild) the command was called in
    # The name of the new channel is "merged-" followed by the names of the two channels being merged
    new_channel = await ctx.guild.create_text_channel(f'merged-{channel1.name}-{channel2.name}')

    # Then, the bot goes through the message history of the first channel from oldest to newest
    async for message in channel1.history(oldest_first=True):
        # For each message, it sends a new message in the new channel
        # This message contains the name of the author of the original message, the time it was sent, and its content
        await new_channel.send(f"{message.author.name} at {message.created_at} said: {message.content}")

    # The bot does the same for the second channel
    async for message in channel2.history(oldest_first=True):
        await new_channel.send(f"{message.author.name} at {message.created_at} said: {message.content}")

bot.run(config['token'])