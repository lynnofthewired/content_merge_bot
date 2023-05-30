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

bot.run(config['token'])

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
