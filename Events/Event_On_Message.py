import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix
from re import search
import sqlite3


class Event_On_Message(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.client.user.id or message.author.guild_permissions.manage_messages:
            return
        db = sqlite3.connect('Data/smiffy_base.db')
        cur = db.cursor()
        cur.execute(f'SELECT * FROM antylink WHERE guild_id = {message.guild.id}')
        res = cur.fetchone()

        if not res:
            return
        if search(self.url_regex, message.content):
            embedchat = discord.Embed(
                title='Wykryto link <:error:919648598713573417>',
                description=f'{message.author} Próbował wysłać link!',
                color=discord.Color.red(),
                timestamp=datetime.utcnow() + timedelta(hours=1)
            )
            await message.channel.send(embed=embedchat)
            await message.delete()
            author = message.author
            embed = discord.Embed(
                title='Ostrzeżenie <a:redalert:919657291639320696>',
                description=f'Na serwerze: **{message.guild}** została nałożona blokada linków.\n'
                            f'Twoja Wiadomość: `{message.content}` została usunięta!',
                color=discord.Color.red(),
                timestamp=datetime.utcnow() + timedelta(hours=1)
            )
            try:
                embed.set_thumbnail(url=message.author.avatar.url)
            except AttributeError:
                pass
            await author.send(embed=embed)


def setup(client):
    client.add_cog(Event_On_Message(client))
