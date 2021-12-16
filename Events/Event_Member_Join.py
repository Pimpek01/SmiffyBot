import nextcord as discord
from nextcord.ext import commands
from nextcord.utils import get
from Commands.settings.CommandLogs import get_log_channel
from datetime import datetime, timedelta
import sqlite3


class Event_Member_Join(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        info = get_log_channel(member)
        if info:
            channel_id = info[1]
            for channel in member.guild.channels:
                if channel.id == channel_id:
                    embed = discord.Embed(
                        title='Nowy Użytkownik Dołączył <a:greenbutton:919647666101694494>',
                        color=discord.Color.yellow(),
                        timestamp=datetime.utcnow() + timedelta(hours=1)
                    )
                    embed.add_field(name='<a:strzalka:919651065597669407> Nazwa', value=f'`{member}`')
                    embed.add_field(name='<a:strzalka:919651065597669407> ID', value=f'`{member.id}`', inline=False)
                    embed.add_field(name='<a:strzalka:919651065597669407> Osoby', value='`{}`'.format(sum(not member.bot for member in member.guild.members)))
                    try:
                        embed.set_thumbnail(url=member.avatar.url)
                    except AttributeError:
                        pass
                    return await channel.send(embed=embed)

        db = sqlite3.connect('Data/smiffy_base.db')
        cur = db.cursor()
        cur.execute(f'SELECT role_id FROM startrole WHERE guild_id = {member.guild.id}')
        res = cur.fetchone()

        if not res:
            return
        role_id = list(res)
        role = get(member.guild.roles, id=role_id[0])
        await member.add_roles(role)
        db.commit()
        cur.close()
        db.close()


def setup(client):
    client.add_cog(Event_Member_Join(client))
