from nextcord.ext import commands
import nextcord as discord
from datetime import datetime, timedelta
from utilities import get_prefix
from asyncio import sleep


class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm', 'h', 'd']:
            return [int(amount), unit]

        raise commands.BadArgument(message='Zła jednostka czasu')


class Command_TempBan(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def tempban(self, ctx, member: discord.Member, duration: DurationConverter, *, reason: str = 'Brak'):
        if ctx.guild.me.top_role <= member.top_role:
            error_embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'**Niestety, ale nie mam wystarczających uprawnień, aby zbanować: **`{member}`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            error_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                error_embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=error_embed)
        if ctx.author.top_role > member.top_role and member != ctx.guild.owner:
            amount, unit = duration
            await member.ban(reason=reason)
            embed = discord.Embed(
                title='Pomyślnie zbanowano <a:greenbutton:919647666101694494>',
                color=discord.Color.green(),
                timestamp=datetime.utcnow() + timedelta(hours=1)
                )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            embed.add_field(name='Użytkownik', value=f'<a:bialastrzalka:919651308124921936> `{member}`')
            embed.add_field(name='Powód', value=f'<a:bialastrzalka:919651308124921936> `{reason}`')
            embed.add_field(name='Czas', value=f'<a:bialastrzalka:919651308124921936> `{amount}{unit}`', inline=False)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            await ctx.send(embed=embed)
            await sleep(amount * self.multiplier[unit])
            await ctx.guild.unban(member)
        else:
            error_embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'**Niestety, ale `{ctx.author}` nie możesz zbanować: `{member}`**',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            error_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                error_embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=error_embed)

    @tempban.error
    async def tempban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Tempban <@member/id> <czas> <powód>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Niestety, ale nie posiadasz permisji: `Ban_Members`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Tempban <@member/id> <czas> <powód>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_TempBan(client))