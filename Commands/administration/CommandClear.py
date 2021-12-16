import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


class Command_Clear(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['purge', 'wyczysc'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, times: int):
        if times > 1000:
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=2),
                color=discord.Color.red(),
                description=f'**Przekroczono limit:** `{times}/1000`')

            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)
        await ctx.message.delete()
        await ctx.channel.purge(limit=times)
        embed = discord.Embed(
            title=f'Pomyślnie usunięto wiadomości <a:greenbutton:919647666101694494>',
            color=discord.Color.lighter_gray(),
            description=f'Usunięte wiadomości: **{times}**',
            timestamp=datetime.utcnow() + timedelta(hours=1),
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=2),
                color=discord.Color.red(),
                description=f'**Poprawne użycie:** `{get_prefix(self.client, ctx)}clear <liczba>`'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=2),
                color=discord.Color.red(),
                description=f'**Poprawne użycie:** `{get_prefix(self.client, ctx)}clear <liczba>`'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=2),
                color=discord.Color.red(),
                description=f'**Niestety, ale nie posiadasz wymaganej permsji:** `Manage_Messages`'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_Clear(client))