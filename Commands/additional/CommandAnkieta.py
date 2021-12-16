import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


class Command_Ankieta(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def ankieta(self, ctx, *, tekst: str):

        embed = discord.Embed(
            title='Nowa ankieta <a:news:919648154075402321>',
            description=f'```{tekst}```',
            color=discord.Color.dark_theme(),
            timestamp=datetime.utcnow() + timedelta(hours=1)
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        message = await ctx.send(embed=embed)

        up = self.client.get_emoji(919647666101694494)
        down = self.client.get_emoji(919647776885850182)
        await message.add_reaction(up)
        await message.add_reaction(down)

    @ankieta.error
    async def ankieta_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Niestety, ale nie posiadasz permisji » `Manage_Channels`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Ankieta <tekst>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_Ankieta(client))
