import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from Commands.settings.CommandLogs import get_log_channel


class Event_Message_Delete(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id != self.client.user.id:
            info = get_log_channel(message)
            if info:
                channel_id = info[1]
                for channel in message.guild.channels:
                    if channel.id == channel_id:
                        async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
                            deleter = entry.user
                            embed = discord.Embed(
                                title='Wiadomość została usunięta <a:redbutton:919647776885850182>',
                                color=discord.Color.dark_gray(),
                                timestamp=datetime.utcnow() + timedelta(hours=1)
                            )
                            embed.add_field(name='<a:strzalka:919651065597669407> Wiadomość', value=f'`{message.content}`')
                            embed.add_field(name='<a:strzalka:919651065597669407> Usuwający', value=f'`{deleter}`', inline=False)
                            embed.set_thumbnail(url=deleter.avatar.url)
                            return await channel.send(embed=embed)


def setup(client):
    client.add_cog(Event_Message_Delete(client))