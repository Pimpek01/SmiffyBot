import nextcord as discord
from nextcord.ext import commands
import sqlite3
from datetime import datetime, timedelta
from utilities import get_prefix


class Command_Warn(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ostrzez'])
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = 'Brak'):
        if ctx.author.top_role >= member.top_role:

            db = sqlite3.connect('Data/smiffy_base.db')
            cur = db.cursor()
            cur.execute(f'SELECT * FROM warnings WHERE guild_id = {ctx.guild.id} and user_id = {member.id}')
            res = cur.fetchone()
            update_warns = 1
            if not res:
                cur.execute(f'INSERT INTO warnings(guild_id, user_id, warns) VALUES(?,?,?)', (ctx.guild.id, member.id, 1))

            if res:
                update_warns = int(res[2]) + 1
                cur.execute(f'UPDATE warnings SET warns = ? WHERE guild_id = ? and user_id = ?', (update_warns, ctx.guild.id, member.id))

            db.commit()
            cur.close()
            db.close()

            embed = discord.Embed(
                title='Pomyślnie nadano ostrzeżenie <a:greenbutton:919647666101694494>',
                color=discord.Color.dark_theme(),
                timestamp=datetime.utcnow() + timedelta(hours=1)
            )
            embed.add_field(name='Użytkownik', value=f'<a:strzalka:868174820653801513> `{member}`', inline=False)
            embed.add_field(name='Powód', value=f'<a:strzalka:868174820653801513> `{reason}`', inline=False)
            embed.add_field(name='Liczba Warnów', value=f'<a:strzalka:868174820653801513> `{update_warns}`', inline=False)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            await ctx.send(embed=embed)

            embed = discord.Embed(
                title='Otrzymałeś warna <a:redalert:919657291639320696>',
                color=discord.Color.red(),
                description=f'**Jest to twój: `{update_warns}` warn.**',
                timestamp=datetime.utcnow() + timedelta(hours=1)
            )
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            embed.add_field(name='Administrator', value=f'<a:strzalka:868174820653801513> `{ctx.author}`', inline=False)
            embed.add_field(name='Powód', value=f'<a:strzalka:868174820653801513> `{reason}`', inline=False)
            embed.add_field(name='Serwer', value=f'<a:strzalka:868174820653801513> `{ctx.guild}`', inline=False)
            await member.send(embed=embed)

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Warn <@member/id> <powód>`',
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
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Warn <@member/id> <powód>`',
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
                description=f'Niestety, ale nie posiadasz permisji » `Kick_Members`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)

    @commands.command(aliases=['usunwarna', 'usunwarny'])
    @commands.has_permissions(kick_members=True)
    async def unwarn(self, ctx, member: discord.Member, amount: int):
        if ctx.author.top_role >= member.top_role:
            db = sqlite3.connect('Data/smiffy_base.db')
            cur = db.cursor()
            cur.execute(f'SELECT * FROM warnings WHERE guild_id = {ctx.guild.id} and user_id = {member.id}')
            res = cur.fetchone()
            if int(res[2]) - amount < 0:
                error_embed = discord.Embed(
                    title='<:error:919648598713573417> Wystąpił błąd.',
                    description=f'**{member}**, nie posiada tylu ostrzeżeń!',
                    timestamp=datetime.utcnow() + timedelta(hours=1),
                    color=discord.Color.red())
                error_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                try:
                    error_embed.set_thumbnail(url=ctx.guild.icon.url)
                except AttributeError:
                    pass
                return await ctx.send(embed=error_embed)

            cur.execute(f'UPDATE warnings SET warns = ? WHERE guild_id = ? and user_id = ?', (int(res[2]) - amount, ctx.guild.id, member.id))
            db.commit()
            cur.close()
            db.close()

            embed = discord.Embed(
                title='Pomyślnie usunięto warny <a:greenbutton:919647666101694494>',
                color=discord.Color.dark_theme(),
                timestamp=datetime.utcnow() + timedelta(hours=1)
            )
            embed.add_field(name='Użytkownik', value=f'<a:bialastrzalka:919651308124921936> `{member}`', inline=False)
            embed.add_field(name='Liczba Warnów', value=f'<a:bialastrzalka:919651308124921936> `{int(res[2]) - amount}`', inline=False)
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            await ctx.send(embed=embed)

            embed = discord.Embed(
                title='Usunięto warny <a:redalert:919657291639320696>',
                color=discord.Color.orange(),
                description=f'**Z twojego konta zabrano: `{amount}` warna/y**',
                timestamp=datetime.utcnow() + timedelta(hours=1)
            )
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            embed.add_field(name='Administrator', value=f'<a:bialastrzalka:919651308124921936> `{ctx.author}`', inline=False)
            embed.add_field(name='Serwer', value=f'<a:bialastrzalka:919651308124921936> `{ctx.guild}`', inline=False)
            await member.send(embed=embed)

    @unwarn.error
    async def unwarn_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Unwarn <@member/id> <Ilość>`',
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
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Unwarn <@member/id> <Ilość>`',
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
                description=f'Niestety, ale nie posiadasz permisji » `Kick_Members`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)

    @commands.command(aliases=['warny'])
    @commands.has_permissions(kick_members=True)
    async def warnings(self, ctx, member: discord.Member):
        db = sqlite3.connect('Data/smiffy_base.db')
        cur = db.cursor()
        cur.execute(f'SELECT * FROM warnings WHERE guild_id = {ctx.guild.id} and user_id = {member.id}')
        res = cur.fetchone()

        warny = 0

        if res:
            warny = res[2]

        embed = discord.Embed(
            title=f'Ostrzeżenia: {member}',
            color=discord.Color.dark_theme(),
            timestamp=datetime.utcnow() + timedelta(hours=1)
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        embed.add_field(name='Liczba warnów', value=f'<a:bialastrzalka:919651308124921936> `{warny}`', inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_Warn(client))
