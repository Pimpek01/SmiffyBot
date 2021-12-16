from nextcord.ext import commands
from io import StringIO
from traceback import format_exc
from textwrap import indent
from contextlib import redirect_stdout


class Command_Eval(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._last_result = None
        self.sessions = set()

    @staticmethod
    def cleanup_code(content: str):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

    @commands.command(pass_context=True, hidden=True)
    @commands.is_owner()
    async def eval(self, ctx, *, body: str):

        env = {
            'bot': self.client,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = StringIO()

        to_compile = f'async def func():\n{indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{format_exc()}\n```')
        else:
            value = stdout.getvalue()
            await ctx.message.add_reaction('\u2705')

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(client):
    client.add_cog(Command_Eval(client))
