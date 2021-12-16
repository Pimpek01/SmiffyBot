import nextcord as discord
from nextcord.ext import commands
from utilities import get_prefix
from datetime import datetime, timedelta
import sqlite3


class Command_Startrole(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['startrole'])
    @commands.has_permissions(manage_channels=True)
    async def startowarola(self, ctx, toggle: str, rola: discord.Role = None):
        if toggle.lower() == 'wlacz':
            if not rola:
                error_embed = discord.Embed(
                    title='<:error:919648598713573417> Wystąpił Błąd.',
                    description=f'Poprawne Użycie: `{get_prefix(self.client, ctx)}startrole <wlacz> <@rola>`',
                    timestamp=datetime.utcnow() + timedelta(hours=1),
                    color=discord.Color.red())
                error_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                try:
                    error_embed.set_thumbnail(url=ctx.guild.icon.url)
                except AttributeError:
                    pass
                return await ctx.send(embed=error_embed)
            if ctx.guild.me.top_role <= rola:
                error_embed = discord.Embed(
                    title='<:error:919648598713573417> Wystąpił Błąd.',
                    description=f'**Podana Rola ma większe uprawnienia ode mnie :(**',
                    timestamp=datetime.utcnow() + timedelta(hours=1),
                    color=discord.Color.red())
                error_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                try:
                    error_embed.set_thumbnail(url=ctx.guild.icon.url)
                except AttributeError:
                    pass
                return await ctx.send(embed=error_embed)
            db = sqlite3.connect('Data/smiffy_base.db')
            cur = db.cursor()
            cur.execute(f'SELECT * FROM startrole WHERE guild_id = {ctx.guild.id}')
            res = cur.fetchone()
            if not res:
                cur.execute(f'INSERT INTO startrole(guild_id, role_id) VALUES(?,?)', (ctx.guild.id, rola.id))

            if res:
                cur.execute(f'UPDATE startrole SET role_id = ? WHERE guild_id = ?', (rola.id, ctx.guild.id))

            db.commit()
            cur.close()
            db.close()

            embed = discord.Embed(
                title='Zaktualizowano StartowaRole <a:greenbutton:919647666101694494>',
                color=discord.Color.dark_theme(),
                timestamp=datetime.utcnow() + timedelta(hours=1),
                description=f'**Rola:** {rola.mention}'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)

        elif toggle.lower() == 'wylacz':
            embed = discord.Embed(
                title='Zaktualizowano StartowaRole <a:greenbutton:919647666101694494>',
                color=discord.Color.dark_theme(),
                timestamp=datetime.utcnow() + timedelta(hours=1),
                description=f'**Rola:** Brak'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            await ctx.send(embed=embed)
            db = sqlite3.connect('Data/smiffy_base.db')
            cur = db.cursor()
            cur.execute(f'SELECT * FROM startrole WHERE guild_id = {ctx.guild.id}')
            res = cur.fetchone()

            if not res:
                return
            cur.execute(f"DELETE from startrole WHERE guild_id = {ctx.guild.id}")

            db.commit()
            cur.close()
            db.close()
            return

    @startowarola.error
    async def startrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił Błąd.',
                description=f'Poprawne Użycie: `{get_prefix(self.client, ctx)}startowarola <wlacz/wylacz> <@rola>`',
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
                title='<:error:919648598713573417> Wystąpił Błąd.',
                description=f'Poprawne Użycie: `{get_prefix(self.client, ctx)}startowarola <wlacz/wylacz> <@rola>`',
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
    client.add_cog(Command_Startrole(client))