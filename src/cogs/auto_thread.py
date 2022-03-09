import asyncio
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


def setup(bot: commands.Bot):
    """
    Setup the cog
    """
    bot.add_cog(AutoQuestionThread(bot))


class SelectQuestionCategory(ui.View):

    def __init__(self, user):
        """
        Initialize
        """
        super().__init__(timeout=60)
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
            self.selected_category = "other"
            self.stop()

    @ui.button(label="キャンセル", style=ButtonStyle.red)
    async def cancelling(self, button: ui.Button, interaction: discord.Interaction):
        """
        Cancel the selection
        """
        if interaction.user == self.user:
            self.stop()


# ------------------------------------------------------------------------------


class AutoConvertThread(commands.Cog):
    channel_id = None

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Listen for messages in the channel
        """
        if self.channel_id == None:
            raise NotImplementedError
        if message.channel.id == self.channel_id:
            if message.author != self.bot.user and not message.is_system():
                await self.make_thread_from_message(message)

    async def make_thread_from_message(self, message: discord.Message):
        """
        Create a thread from a message
        """
        raise NotImplementedError


class AutoQuestionThread(AutoConvertThread):
    channel_id = 419507067406254081 # 本番
    # channel_id = 941175111845822506  # 実験用
    # channel_id = 941023971263004722 # デバッグ用

    async def make_thread_from_message(self, message: discord.Message):
        title = "自動スレッド化"
        delete_time = 30

        # Ask the user to select a category
        e = Embed(
            title=title,
            description="質問有難うございます! この質問のカテゴリーを教えてください",
        )
        v = SelectQuestionCategory(message.author)
        m = await message.reply(embed=e, view=v)
        timeouted = await v.wait()
        if timeouted:
            await m.edit(embed=Embed(title=title, description=f"タイムアウトしたため、質問のスレッド化をキャンセルしました。なお、このメッセージと質問文は{delete_time}秒後に削除されます。", color=0xFF0000), view=None)
            await asyncio.sleep(delete_time)
            await m.delete()
            try:
                await message.delete()
            except discord.NotFound as e:
                pass
            return

        sc = v.selected_category
        if sc is None:  # Cancelled
            await m.edit(embed=Embed(title=title, description=f"質問のスレッド化をキャンセルしました。なお、このメッセージと質問文は{delete_time}秒後に削除されます。", color=0xFF0000))
            await asyncio.sleep(delete_time)
            await message.delete()
            await m.delete()
            return

        msc = categories[sc]
        c = message.channel
        attachments = message.attachments
        files = [await f.to_file() for f in attachments] if attachments else []

        tm = await c.send(embed=Embed(
            title=f"【{msc}】についての質問",
            description=f"{message.author.mention}さんからの質問です。\n",
            url=""
        ))
        t = await tm.create_thread(
            name=f"【{msc}】{message.content}"
        )
        await t.add_user(message.author)
        e = Embed(
            title=f"{msc} - {message.author.display_name} さんから",
            description=message.content,
            url=""
        )
        e.set_author(name=message.author.display_name,
                     icon_url=message.author.display_avatar.url)

        await t.send(content=f"{message.author.mention} スレッドを作成しました! 以降はこのスレッドで質問をお願いします。", embed=e)

        for f in files:
            e = Embed(
                title="",
                description=f"{msc} - {message.author.display_name} さんから",
                url=""
            )
            e.set_image(url=f"attachment://{f.filename}")
            e.set_author(name=message.author.display_name,
                         icon_url=message.author.display_avatar.url)
            await t.send(file=f, embed=e)
        # e.set_footer(text="問題が解決しましたら、下のボタンを押してください")

        # Notify the author that the thread was created successfully
        await m.edit(
            embed=Embed(
                title=title, description=f"スレッドを作成しました! 以降はこのスレッドで質問をお願いします。\nなお、このスレッドと質問文は{delete_time}秒後に削除されます。",
                color=0x00FF00
            ), view=discord.ui.View())
        await asyncio.sleep(delete_time)
        await message.delete()
        await m.delete()
