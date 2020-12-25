# -*- encoding:utf-8 -*-
import asyncio
from pprint import pprint

import discord
from pymongo import MongoClient

import config.settings as config

from discord.ext import commands

from core.kagura import Kagura


async def get_prefix(bot, message):
    # extras = config.TOKEN
    return commands.when_mentioned_or(config.prefix)(bot, message)


# Instantion bot
bot = Kagura(
    case_insensitive=True,
    command_prefix=get_prefix,
    owner_id=319842407829078016,
    member_cache_flags=True
)


@bot.check
async def legacy(ctx):
    if ctx.author.id == 319842407829078016:
        return True
    else:
        return True


@bot.check
async def cmd_check(ctx):
    if ctx.author.bot:
        return False
    if isinstance(ctx.channel, discord.DMChannel):
        return True
    if ctx.command.cog.__class__.__name__ == 'Jishaku':
        return True

    return True


async def run():
    # He need dnspython for parse url srv
    clientMongo = MongoClient(
        f'mongodb://{config.MONOGO_USERNAME}:{config.MONOGO_PASS}@{config.MONOGO_HOST}/{config.MONOGO_DB_NAME}?{"authSource=ascencia&" if config.MONOGO_DB_NAME is not None else ""}retryWrites=true&w=majority'
    )

    bot.db = clientMongo.ascencia
    await bot.start(config.token)


async def stop():
    await bot.logout()


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(run())
    except KeyboardInterrupt:
        asyncio.get_event_loop().run_until_complete(stop())
