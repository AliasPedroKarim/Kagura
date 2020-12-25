# -*- encoding:utf-8 -*-
import discord
from discord.ext.commands import check, NotOwner


def is_owner():
    """
    A :func:`.check` that checks if the person invoking this command is the
    owner of the bot.

    This is powered by :meth:`.Bot.is_owner`.

    This check raises a special exception, :exc:`.NotOwner` that is derived
    from :exc:`.CheckFailure`.
    """

    async def predicate(ctx):
        if not await ctx.bot.is_owner(ctx.author):
            embed = discord.Embed()

            embed.set_author(name=f' | You do not own this bot.', url=ctx.author.avatar_url,
                             icon_url=ctx.author.avatar_url)

            await ctx.channel.send(embed=embed)
            raise NotOwner(f"({ctx.author.name}#{ctx.author.discriminator} | {str(ctx.author.id)}) to run a system that shouldn't.")
        return True

    return check(predicate)
