import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from Commands.settings.CommandLogs import get_log_channel


class EventMemberRemove(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        info = get_log_channel(member)
        if info:
            channel_id = info[1]
            channel = self.client.get_channel(channel_id)
            embed = discord.Embed(
                title='Użytkownik wyszedł <a:redbutton:919647776885850182>',
                color=discord.Color.red(),
                timestamp=datetime.utcnow() + timedelta(hours=1)
            )
            embed.add_field(name='<a:strzalka:919651065597669407> Nazwa', value=f'`{member}`')
            embed.add_field(name='<a:strzalka:919651065597669407> ID', value=f'`{member.id}`', inline=False)
            embed.add_field(name='<a:strzalka:919651065597669407> Osoby', value='`{}`'.format(sum(not member.bot for member in member.guild.members)))
            embed.set_thumbnail(url=member.avatar.url)
            await channel.send(embed=embed)


def setup(client):
    client.add_cog(EventMemberRemove(client))

