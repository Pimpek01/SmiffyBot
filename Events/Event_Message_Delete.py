import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from Commands.settings.CommandLogs import get_log_channel


class EventMessageDelete(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id != self.client.user.id:
            info = get_log_channel(message)
            if info:
                channel_id = info[1]
                channel = self.client.get_channel(channel_id)
                embed = discord.Embed(
                    title='Wiadomość została usunięta <a:redbutton:919647776885850182>',
                    color=discord.Color.dark_gray(),
                    timestamp=datetime.utcnow() + timedelta(hours=1)
                    )
                embed.add_field(name='<a:strzalka:919651065597669407> Wiadomość', value=f'`{message.content}`')
                try:
                    embed.set_thumbnail(url=message.guild.icon.url)
                except AttributeError:
                    pass
                return await channel.send(embed=embed)


def setup(client):
    client.add_cog(EventMessageDelete(client))
