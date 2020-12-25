# -*- encoding:utf-8 -*-
from pprint import pprint

import discord
from discord.ext import commands


class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stats',
                      description='This command displays information about the bot connection time.',
                      aliases=['statistics'])
    async def stats(self, ctx, member: discord.Member = None):

        # Fetch Member
        if not member:
            member = ctx.author
        else:
            member = ctx.guild.get_member(member.id)

        data_user = self.bot.db.users.find_one({"user_id": f'{member.id}'})

        if not data_user:
            ctx.channel.send(f'The **{member.display_name}#{member.discriminator}** user does not have any XP on all the servers to my knowledge.')
        else:
            embed = discord.Embed()
            embed.set_author(
                name=f'Globals Stats Leveling for {member.display_name}#{member.discriminator}',
                icon_url=ctx.guild.icon_url
            )

            embed.set_footer(text=f'{member.display_name}#{member.discriminator} - © {ctx.bot.user.display_name}', icon_url=member.avatar_url)

            for guild_id in data_user['guilds']:
                guild_level = data_user['guilds'][guild_id]
                if guild_level['levels'] is not None:
                    level = guild_level["levels"]["level"]
                    xp = guild_level["levels"]["xp"]
                    max = guild_level["levels"]["max"]
                    embed.add_field(
                        name=f'Server: {guild_level["name"]}',
                        value=f'**{str(level)}** Level **·** **{str(xp)}** XP\nMax: **{str(max)}** **·** Remainder: **{str(max - xp)}** **·** Pourcentage: **{str(round(xp / max * 100, 2))}**%',
                        inline=False
                    )

            await ctx.channel.send(embed=embed)


def setup(bot):
    try:
        bot.add_cog(Stats(bot))
        bot.logger.info(f'$GREENLoaded $BLUE"stats" $GREENcommand!')
    except Exception as e:
        bot.logger.error(f'$REDError while adding command $BLUE"stats"', exc_info=e)
