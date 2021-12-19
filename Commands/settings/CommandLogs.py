import nextcord as discord
from nextcord.ext import commands
import sqlite3
from datetime import datetime, timedelta
from utilities import get_prefix


def get_log_channel(ctx) -> tuple[int, int]:
    db = sqlite3.connect('Data/smiffy_base.db')
    cur = db.cursor()
    cur.execute(f'SELECT * FROM Logs WHERE guild_id = {ctx.guild.id}')
    res = cur.fetchone()
    return res


class Command_Log(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def logi(self, ctx, toggle: str, channel: discord.TextChannel = None):

        if toggle.lower() == 'wlacz':
            if not channel:
                embed = discord.Embed(
                    title='<:error:919648598713573417> Wystąpił Błąd.',
                    timestamp=datetime.utcnow() + timedelta(hours=2),
                    color=discord.Color.red(),
                    description=f'**Poprawne Uzycie:** `{get_prefix(self.client, ctx)}Logi <Wlacz/Wylacz> <#Kanał>`'
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                try:
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                except AttributeError:
                    pass
                await ctx.send(embed=embed)
            db = sqlite3.connect('Data/smiffy_base.db')
            cur = db.cursor()
            cur.execute(f'SELECT * FROM Logs WHERE guild_id = {ctx.guild.id}')
            res = cur.fetchone()

            if not res:
                cur.execute(f'INSERT INTO Logs(guild_id, channel_id) VALUES(?,?)', (ctx.guild.id, channel.id))

            if res:
                cur.execute(f'UPDATE Logs SET channel_id = ? WHERE guild_id = ?', (channel.id, ctx.guild.id))

            db.commit()
            cur.close()
            db.close()

            embed = discord.Embed(
                title='Pomyślnie Włączono Logi <a:greenbutton:919647666101694494>',
                color=discord.Color.green(),
                timestamp=datetime.utcnow() + timedelta(hours=1)
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            return await ctx.reply(embed=embed)

        elif toggle.lower() == 'wylacz':

            db = sqlite3.connect('Data/smiffy_base.db')
            cur = db.cursor()
            cur.execute(f'SELECT * FROM Logs WHERE guild_id = {ctx.guild.id}')
            res = cur.fetchone()

            if not res:
                embed = discord.Embed(
                    title='<:error:919648598713573417> Wystąpił Błąd.',
                    description=f'**Logi** na serwerze już są wyłączone!',
                    timestamp=datetime.utcnow() + timedelta(hours=1),
                    color=discord.Color.red())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                try:
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                except AttributeError:
                    pass
                return await ctx.send(embed=embed)

            if res:
                cur.execute(f"DELETE from Logs WHERE guild_id = {ctx.guild.id}")

            db.commit()
            cur.close()
            db.close()

            embed = discord.Embed(
                title='Pomyślnie Wyłączono Logi <a:greenbutton:919647666101694494>',
                color=discord.Color.green(),
                timestamp=datetime.utcnow() + timedelta(hours=1)
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            return await ctx.reply(embed=embed)
        embed = discord.Embed(
            title='<:error:919648598713573417> Wystąpił Błąd.',
            timestamp=datetime.utcnow() + timedelta(hours=1),
            color=discord.Color.red(),
            description=f'**Poprawne Uzycie:** `{get_prefix(self.client, ctx)}Logi <Wlacz/Wylacz> <#Kanał>`'
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        await ctx.send(embed=embed)

    @logi.error
    async def logi_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił Błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red(),
                description=f'**Poprawne Uzycie:** `{get_prefix(self.client, ctx)}Logi <Wlacz/Wylacz> <#Kanał>`'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)

        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił Błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red(),
                description=f'**Poprawne Uzycie:** `{get_prefix(self.client, ctx)}Logi <Wlacz/Wylacz> <#Kanał>`'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)

        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił Błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=2),
                color=discord.Color.red(),
                description=f'Niestety, ale nie posiadasz permisji » `Manage_Channels`'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_Log(client))