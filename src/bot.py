import os
import json
import discord
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix='¥')

with open("src/config.json") as f:
    config = json.load(f)


def register_cogs():
    """
    Register all cogs in the cogs folder
    """
    for filename in os.listdir('./src/cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'src.cogs.{filename[:-3]}')


if __name__ == "__main__":
    token = os.environ.get('DISCORD_TOKEN')
    bot.run(token)
