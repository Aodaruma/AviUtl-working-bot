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
            try:
                bot.load_extension(f'cogs.{filename[:-3]}')
            except discord.ExtensionAlreadyLoaded as e:
                pass


if __name__ == "__main__":
    token = os.environ.get('DISCORD_TOKEN')
    bot.run(token)
