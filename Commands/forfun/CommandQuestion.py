from nextcord.ext import commands
import nextcord as discord
from datetime import datetime, timedelta
from random import choice
from utilities import get_prefix


class Command_Pytanie(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.answers: tuple = ('Tak', 'Nie', 'Raczej, Nie', 'Raczej, Tak')

    @commands.command()
    async def pytanie(self, ctx, *, pytanie: str):
        embed = discord.Embed(description=f'Pytanie: **{pytanie}**\nOdpowiedź: **{choice(self.answers)}**',
                              color=discord.Color.dark_theme(),
                              timestamp=datetime.utcnow() + timedelta(hours=1))
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @pytanie.error
    async def pytanie_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił Błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=2),
                color=discord.Color.red(),
                description=f'**Poprawne Uzycie:** `{get_prefix(self.client, ctx)}pytanie <tekst>`'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_Pytanie(client))