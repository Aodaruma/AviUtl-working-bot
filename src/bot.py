import os
import json
import dotenv
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


def unregister_cogs():
    """
    Unregister all cogs in the cogs folder
    """
    for filename in os.listdir('./src/cogs'):
        if filename.endswith('.py'):
            try:
                bot.unload_extension(f'cogs.{filename[:-3]}')
            except discord.ExtensionNotLoaded as e:
                pass


@bot.event
async def on_ready():
    """
    When the bot is ready
    """
    print(f'Logged in as {bot.user}')
    register_cogs()


@bot.command()
async def ping(ctx):
    """
    Ping
    """
    await ctx.send(f'pong! {round(bot.latency * 1000)}ms')


@bot.command()
@commands.is_owner()
async def reload(ctx):
    """
    Reload all cogs
    """
    unregister_cogs()
    register_cogs()
    await ctx.send('Reloaded all cogs')

if __name__ == "__main__":
    dotenv.load_dotenv("src/.env")
    token = os.environ.get('DISCORD_TOKEN')
    bot.run(token)
