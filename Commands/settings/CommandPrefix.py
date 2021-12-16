import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix
import sqlite3


class Command_Prefix(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ustawprefix', 'setprefix'])
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, new_prefix: str):
        if len(new_prefix) > 8:
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił Błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red(),
                description='Prefix Nie Może Przekraczać **8** liter!'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)

        old_prefix = get_prefix(self.client, ctx)
        if old_prefix == '':
            old_prefix = 'Invisible!'
        db = sqlite3.connect('Data/smiffy_base.db')
        c = db.cursor()
        c.execute(f'SELECT * FROM prefixes WHERE guild_id = {ctx.guild.id}')
        res = c.fetchone()

        if not res:
            c.execute(f'INSERT INTO prefixes(guild_id, prefix) VALUES(?,?)', (ctx.guild.id, new_prefix))

        if res:
            c.execute(f'UPDATE prefixes SET prefix = ? WHERE guild_id = ?', (new_prefix, ctx.guild.id))

        db.commit()
        c.close()
        db.close()

        embed = discord.Embed(
            title='Pomyslnie Zaktualizowano Prefix <a:greenbutton:919647666101694494>',
            color=discord.Color.green(),
            timestamp=datetime.utcnow() + timedelta(hours=2),
        )
        embed.add_field(name='Poprzedni Prefix', value=f'`{old_prefix}`')
        embed.add_field(name='Aktualny Prefix', value=f'`{new_prefix}`', inline=True)
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił Błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red(),
                description='**Niestety, ale nie posiadasz wymaganej permsji:** `Manage_Guild`'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił Błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red(),
                description=f'**Poprawne Uzycie:** `{get_prefix(self.client, ctx)}prefix <tekst>`'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_Prefix(client))
