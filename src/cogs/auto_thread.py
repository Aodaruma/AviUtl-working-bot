import discord
from discord.ext import commands, tasks
from discord import ui, ButtonStyle, Embed
# from discord.ext import ui
# from discord.ext.ui import Message, Button

categories = {
    "errors_and_bugs": "エラーやバグ",
    "showing_and_technical": "表現系・技術系",
    "tips": "豆知識",
    "programming": "プログラミング",
    "other": "その他"
}


class SelectQuestionCategory(ui.View):

    def __init__(self, user):
        """
        Initialize
        """
        super().__init__()
        self.selected_category = None
        self.user = user

    @ui.button(label=categories["errors_and_bugs"])
    async def ask_about_errors_button(self, button: ui.Button, interaction: discord.Interaction):
        """
        Set the selected category to Error and Bugs
        """
        if interaction.user == self.user:
            self.selected_category = "errors_and_bugs"
            self.stop()

    @ui.button(label=categories["showing_and_technical"])
    async def ask_about_showing_button(self, button: ui.Button, interaction: discord.Interaction):
        """
        Set the selected category to Showing and Technical
        """
        if interaction.user == self.user:
            self.selected_category = "showing_and_technical"
            self.stop()

    @ui.button(label=categories["tips"])
    async def ask_about_tips_button(self, button: ui.Button, interaction: discord.Interaction):
        """
        Set the selected category to Tips
        """
        if interaction.user == self.user:
            self.selected_category = "tips"
            self.stop()

    @ui.button(label=categories["programming"])
    async def ask_about_programming_button(self, button: ui.Button, interaction: discord.Interaction):
        """
        Set the selected category to Programming
        """
        if interaction.user == self.user:
            self.selected_category = "programming"
            self.stop()

    @ui.button(label=categories["other"])
    async def ask_about_others_button(self, button: ui.Button, interaction: discord.Interaction):
        """
        Set the selected category to Others
        """
        if interaction.user == self.user:
            self.selected_category = "others"
            self.stop()

    @ui.button(label="キャンセル", style=ButtonStyle.red)
    async def cancelling(self, button: ui.Button, interaction: discord.Interaction):
        """
        Cancel the selection
        """
        if interaction.user == self.user:
            self.stop()



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
