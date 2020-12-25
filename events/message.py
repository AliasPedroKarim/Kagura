# -*- encoding:utf-8 -*-
import discord
from discord.ext import commands


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if not isinstance(message.author, discord.Member):
            return
        if message.author.bot:
            return


def setup(bot):
    try:
        bot.add_cog(Message(bot))
        bot.logger.info(f'$GREENLoaded event $BLUEMessage!')
    except Exception as e:
        bot.logger.error(f'$REDError while loading event $BLUE"Message"', exc_info=e)
