import nextcord
from nextcord.ext import commands
import sqlite3


class Event_Guild_Join(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db = sqlite3.connect('Data/smiffy_base.db')
        c = db.cursor()
        c.execute(f'SELECT * FROM prefixes WHERE guild_id = {guild.id}')
        res = c.fetchone()

        if not res:
            c.execute('INSERT INTO prefixes(guild_id, prefix) VALUES(?,?)', (guild.id, 's!'))

        if res:
            c.execute('UPDATE prefixes SET prefix = ? WHERE guild_id = ?', ('s!', guild.id))
        db.commit()
        c.close()
        db.close()


def setup(client):
    client.add_cog(Event_Guild_Join(client))