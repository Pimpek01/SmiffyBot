import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from Commands.settings.CommandLogs import get_log_channel


class EventMessageEdit(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.name == self.client.user.name:
            return
        if before.content != after.content:
            info = get_log_channel(after)
            if info:
                channel_id = info[1]
                for channel in after.guild.channels:
                    if channel.id == channel_id:
                        embed = discord.Embed(
                            title='Wiadomość została zedytowana <a:greenbutton:919647666101694494>',
                            color=discord.Color.darker_grey(),
                            timestamp=datetime.utcnow() + timedelta(hours=1)
                        )
                        embed.add_field(name='<a:strzalka:919651065597669407> Wcześniej', value=f'`{before.content}`')
                        embed.add_field(name='<a:strzalka:919651065597669407> Aktualnie', value=f'`{after.content}`', inline=False)
                        embed.add_field(name='<a:strzalka:919651065597669407> Użytkownik', value=f'`{after.author}`')
                        embed.set_thumbnail(url=after.author.avatar.url)
                        return await channel.send(embed=embed)


def setup(client):
    client.add_cog(EventMessageEdit(client))
