import nextcord as discord
from nextcord.ext import commands
from io import BytesIO
from aiohttp import ClientSession
from utilities import get_prefix
from datetime import datetime, timedelta


class CommandTrump(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def trump(self, ctx, *, text: str):
        async with ClientSession() as session:
            async with session.get(f'https://api.no-api-key.com/api/v2/trump?message={text}') as resp:
                if resp.status != 200:
                    return
                data = BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'cool_image.png'))

    @trump.error
    async def trump_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił Błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=2),
                color=discord.Color.red(),
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}trump <Tekst>`',
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass


def setup(client):
    client.add_cog(CommandTrump(client))