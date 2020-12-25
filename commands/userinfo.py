# -*- encoding:utf-8 -*-
import discord
import typing
from datetime import datetime
from discord.ext import commands

from utils.helpers import diff_month


class UserInfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userinfo',
                      description='This command displays information about user.',
                      aliases=['ui', 'whois'])
    async def stats(self, ctx, user: typing.Union[discord.Member, discord.User] = None):
        if not user:
            user = ctx.author

        # Val
        user_tag = f'{user.name}#{user.discriminator}'
        badges = self.get_badges(user)

        #
        # members_sorted = ctx.guild.members.sort(key=lambda x: x.joined_at)
        #
        # user_index = members_sorted.index()

        # Embed
        embed = discord.Embed()
        embed.set_author(name=f'{user.name}\'s User and Member Information', icon_url=user.avatar_url)

        if badges:
            embed.description = ' **·** '.join(badges) + '\n'

        embed.add_field(name='User information',
                        value='Username: **%s**\nCreated at: **%s**\nIs bot: %s\nMention: %s\nStatus: %s' % (
                            user_tag,
                            user.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
                            ('\✅' if user.bot == True else '\❌'),
                            user.mention,
                            str(discord.utils.get(self.bot.emojis, id=(
                                723297360163111267 if str(user.status) == 'online' else (
                                    661984420001218560 if str(user.status) == 'idle' else (
                                        661984419589914628 if str(user.status) == 'dnd' else 661984419971727381)))))
                        ),
                        inline=False)
        embed.add_field(name=f'Member information ({user.guild.name})',
                        value='%s%s%s%s' % (
                            ('Nickname: **' + user.nick + '**' if user.nick else ''),
                            f'\nJoined at: **{user.joined_at.strftime("%m/%d/%Y, %H:%M:%S")}**',
                            ('' if user.premium_since is None else f'\nNitro booster: {self.premium_guild_since(user.premium_since)}'),
                            f"\nHighest Role: {user.top_role.mention}"
                        ),
                        inline=False)

        embed.set_thumbnail(url=user.avatar_url)
        await ctx.channel.send(embed=embed)

    def get_badges(self, user: typing.Union[discord.User, discord.Member]):
        badge_checks = {
            'staff': discord.utils.get(
                self.bot.emojis, id=706961734245679104),
            'partner': discord.utils.get(
                self.bot.emojis, id=759836708597923860),
            'hypesquad': discord.utils.get(
                self.bot.emojis, id=706961734216319006),
            'bug_hunter': discord.utils.get(
                self.bot.emojis, id=706961734014992464),
            'bug_hunter_level_2': discord.utils.get(
                self.bot.emojis, id=706961734014992464),
            'early_supporter': discord.utils.get(
                self.bot.emojis, id=706961733930975354),
            'verified_bot': discord.utils.get(
                self.bot.emojis, id=715575370010722345),
            'verified_bot_developer': discord.utils.get(
                self.bot.emojis, id=706961734300073994),
            'hypesquad_bravery': discord.utils.get(
                self.bot.emojis, id=706961733863997470),
            'hypesquad_brilliance': discord.utils.get(
                self.bot.emojis, id=706961733994020956),
            'hypesquad_balance': discord.utils.get(
                self.bot.emojis, id=706964242510774313)
        }
        badges = [str(v) for k, v in badge_checks.items() if getattr(user.public_flags, k)]
        # if user.id in self.bot.premium_guilds.values():
        #     badges.append(str(discord.utils.get(
        #         self.bot.emojis, id=680519037704208466)))
        # if badges:
        #     badges.append(u'\u200b')  # Prevents huge emojis on mobile

        return badges

    def premium_guild_since(self, date_premium):
        amount_month = diff_month(datetime.now(), date_premium)

        if amount_month > 24:
            return str(discord.utils.get(self.bot.emojis, id=723297359307473027))
        elif amount_month > 18:
            return str(discord.utils.get(self.bot.emojis, id=723297360490266754))
        elif amount_month > 15:
            return str(discord.utils.get(self.bot.emojis, id=723297359651405844))
        elif amount_month > 12:
            return str(discord.utils.get(self.bot.emojis, id=723297361119412344))
        elif amount_month > 9:
            return str(discord.utils.get(self.bot.emojis, id=723297359605268613))
        elif amount_month > 6:
            return str(discord.utils.get(self.bot.emojis, id=723297360574283826))
        elif amount_month > 3:
            return str(discord.utils.get(self.bot.emojis, id=723297359416787045))
        elif amount_month > 2:
            return str(discord.utils.get(self.bot.emojis, id=723297359592685661))
        else:
            return str(discord.utils.get(self.bot.emojis, id=723297360163111267))

def setup(bot):
    try:
        bot.add_cog(UserInfo(bot))
        bot.logger.info(f'$GREENLoaded $BLUE"userinfo" $GREENcommand!')
    except Exception as e:
        bot.logger.error(f'$REDError while adding command $BLUE"userinfo"', exc_info=e)
