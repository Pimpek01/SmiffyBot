import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix
import sqlite3


class Command_AntyLink(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def antylink(self, ctx, toggle):
        if toggle == 'wlacz':
            db = sqlite3.connect('Data/smiffy_base.db')
            cur = db.cursor()
            cur.execute(f'SELECT * FROM antylink WHERE guild_id = {ctx.guild.id}')
            res = cur.fetchone()
            if not res:
                cur.execute(f'INSERT INTO antylink(guild_id, enabled) VALUES(?,?)', (ctx.guild.id, "true"))

            if res:
                embed = discord.Embed(
                    title='<:error:919648598713573417> Wystąpił Błąd.',
                    description=f'Blokada Linków Już Jest Włączona',
                    timestamp=datetime.utcnow() + timedelta(hours=1),
                    color=discord.Color.red())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                try:
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                except AttributeError:
                    pass
                return await ctx.send(embed=embed)

            db.commit()
            cur.close()
            db.close()

            embed = discord.Embed(
                title='Pomyślnie Włączono <a:greenbutton:919647666101694494>',
                color=discord.Color.dark_theme(),
                description='Blokada Linków Została Włączona',
                timestamp=datetime.utcnow() + timedelta(hours=1),
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)

        elif toggle == 'wylacz':
            db = sqlite3.connect('Data/smiffy_base.db')
            cur = db.cursor()
            cur.execute(f'SELECT * FROM antylink WHERE guild_id = {ctx.guild.id}')
            res = cur.fetchone()

            if not res:
                embed = discord.Embed(
                    title='<:error:919648598713573417> Wystąpił Błąd.',
                    description=f'Blokada Linków Już Jest Wyłączona',
                    timestamp=datetime.utcnow() + timedelta(hours=1),
                    color=discord.Color.red())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                try:
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                except AttributeError:
                    pass
                return await ctx.send(embed=embed)
            cur.execute(f"DELETE from antylink WHERE guild_id = {ctx.guild.id}")

            db.commit()
            cur.close()
            db.close()

            embed = discord.Embed(
                title='Pomyślnie Wyłączono <a:greenbutton:919647666101694494>',
                color=discord.Color.dark_theme(),
                description='Blokada Linków Została Wyłączona',
                timestamp=datetime.utcnow() + timedelta(hours=1),
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)
        embed = discord.Embed(
            title='<:error:919648598713573417> Wystąpił Błąd.',
            description=f'Poprawne Użycie: `{get_prefix(self.client, ctx)}Antylink <wlacz/wylacz>`',
            timestamp=datetime.utcnow() + timedelta(hours=1),
            color=discord.Color.red())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        return await ctx.send(embed=embed)

    @antylink.error
    async def antylink_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił Błąd.',
                description=f'Poprawne Użycie: `{get_prefix(self.client, ctx)}Antylink <wlacz/wylacz>`',
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
                title='<:error:919648598713573417> Wystąpił Błąd.',
                description=f'Niestety, ale nie posiadasz permisji » `Manage_Channels`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_AntyLink(client))