# -*- encoding:utf-8 -*-
import datetime

import discord
from discord.ext import commands


class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', description='This command displays information about the bot connection time.', aliases=['pg'])
    async def ping(self, ctx):
        await ctx.channel.trigger_typing()

        latency = round(self.bot.latency * 1000)
        start = round(datetime.datetime.utcnow().timestamp() * 1000)
        msg = await ctx.send(content='Ping <a:lalalala:501157548783566859>...')
        end = round(datetime.datetime.utcnow().timestamp() * 1000)
        elapsed = round(end - start)

        embed = discord.Embed()
        embed.set_author(name=f'Pong... | 📩 • Message {elapsed}ms | 📈 • WebSocket {latency}ms', url=ctx.author.avatar_url, icon_url=ctx.author.avatar_url)

        await msg.delete(delay=1)
        await ctx.send(embed=embed)


def setup(bot):
    try:
        bot.add_cog(Ping(bot))
        bot.logger.info(f'$GREENLoaded $BLUE"ping" $GREENcommand!')
    except Exception as e:
        bot.logger.error(f'$REDError while adding command $BLUE"ping"', exc_info=e)
