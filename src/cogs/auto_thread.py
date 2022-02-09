import discord
from discord.ext import commands, tasks


class AutoThread(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pages = [
            discord.Embed(title="質問を投稿するには、以下のコマンドを使用してください。",
                          description="", color=0x00ff00),
        ]

    @property
    def channel_id(self) -> int:
        """
          Get the channel ID from the config file
        """
        raise NotImplementedError

    @commands.Cog.listener()
    async def on_message(self, message):
        """
          Listen for messages in the channel
        """
        if message.channel.id == self.channel_id:
            await self.bot.make_thread_from_message(message)

    async def make_thread_from_message(self, message: discord.Message):
        """
          Create a thread from a message
        """
        await message.reply(f"質問ありがとうございます!\nこの質問のカテゴリを教えてください:")
        await self.

        await c.create_thread(recipient=message.author, content=f"Question: {m}")
