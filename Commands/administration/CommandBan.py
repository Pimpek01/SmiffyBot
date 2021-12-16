import nextcord as discord
from nextcord.ext import commands
from utilities import get_prefix
from datetime import datetime, timedelta


class CommandBan(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = 'Brak'):
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
            await member.ban(reason=reason)
            embed = discord.Embed(
                title='Pomyślnie zbanowano <a:greenbutton:919647666101694494>',
                color=discord.Color.green(),
                timestamp=datetime.utcnow() + timedelta(hours=1)
                )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            embed.add_field(name='Użytkownik', value=f'<a:bialastrzalka:919651308124921936> `{member}`')
            embed.add_field(name='Powód', value=f'<a:bialastrzalka:919651308124921936> `{reason}`')
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            await ctx.send(embed=embed)

            pv_embed = discord.Embed(
                title='Zostałeś zbanowany <a:redalert:919657291639320696>',
                color=discord.Color.dark_orange(),
                timestamp=datetime.utcnow() + timedelta(hours=1)
            )
            pv_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            pv_embed.add_field(name='Administrator', value=f'<a:bialastrzalka:919651308124921936> `{ctx.author}`')
            pv_embed.add_field(name='Powód', value=f'<a:bialastrzalka:919651308124921936> `{reason}`')
            pv_embed.add_field(name='Serwer', value=f'<a:bialastrzalka:919651308124921936> `{ctx.guild}`', inline=False)
            try:
                pv_embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return member.send(embed=embed)
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

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}ban <@member/id> <powód>`',
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
                description=f'Niestety, ale nie posiadasz permisji » `Ban_Members`',
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
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}ban <@member/id> <powód>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CommandBan(client))
