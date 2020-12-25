# -*-coding:utf-8 -*
import ast
import discord

from discord.ext import commands

from utils import helpers, overwrite


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class Py(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='This command displays information about the bot connection time.',
                      aliases=['python'])
    @overwrite.is_owner()
    async def py(self, ctx, *, cmd):
        """
        Evaluates input.
        Input is interpreted as newline seperated statements.
        If the last statement is an expression, that is the return value.
        Usable globals:
          - `bot`: the bot instance
          - `discord`: the discord module
          - `commands`: the discord.ext.commands module
          - `ctx`: the invokation context
          - `__import__`: the builtin `__import__` function
        Such that `>eval 1 + 1` gives `2` as the result.
        The following invokation will cause the bot to send the text '9'
        to the channel of invokation and return '3' as the result of evaluating
        >eval ```
            a = 1 + 2
            b = a * 2
            await ctx.send(a + b)
            a
        ```
        """
        try:
            fn_name = "_eval_expr"

            cmd = cmd.strip("` ")

            # add a layer of indentation
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

            # wrap in async def body
            body = f"async def {fn_name}():\n{cmd}"

            parsed = ast.parse(body)
            body = parsed.body[0].body

            insert_returns(body)

            env = {
                'bot': ctx.bot,
                'discord': discord,
                'commands': commands,
                'ctx': ctx,
                '__import__': __import__
            }

            exec(compile(parsed, filename="<ast>", mode="exec"), env)

            result = (await eval(f"{fn_name}()", env))

            await ctx.send(
                content=f'**Evaluted source code**\nInput:\n{helpers.md_code(cmd.strip())}\nOutput:\n{helpers.md_code(str(result)[:1000])}\nType:\n{type(result)}')
        except Exception as e:
            await ctx.send(
                content=f'**An error occurred while executing the code**\nInput:\n{helpers.md_code(cmd.strip())}\nError message:\n{helpers.md_code(str(e)[:1000])}\nType:\n{type(e)}')


def setup(bot):
    try:
        bot.add_cog(Py(bot))
        bot.logger.info(f'$GREENLoaded $BLUE"py" $GREENcommand!')
    except Exception as e:
        bot.logger.error(f'$REDError while adding command $BLUE"py"', exc_info=e)
