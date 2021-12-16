import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from Commands.settings.CommandLogs import get_log_channel


class Event_User_Update(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        user = None
        for guild in self.client.guilds:
            for member in guild.members:
                if member.id == after.id:
                    user = member
        if user:
            info = get_log_channel(user)
            if info:
                channel_id = info[1]
                if before.name != after.name:
                    embed = discord.Embed(
                        title='Użytkownik zmienił nazwę <a:greenbutton:919647666101694494>',
                        color=discord.Color.from_rgb(108, 175, 164),
                        timestamp=datetime.utcnow() + timedelta(hours=1)
                            )
                    embed.add_field(name='<a:strzalka:919651065597669407> Wcześniej', value=f'`{before.name}`', inline=False)
                    embed.add_field(name='<a:strzalka:919651065597669407> Aktualnie', value=f'`{after.name}`', inline=False)
                    embed.add_field(name='<a:strzalka:919651065597669407> Użytkownik', value=f'`{user}`')
                    embed.set_thumbnail(url=user.avatar.url)

                    for channel in user.guild.channels:
                        if channel.id == channel_id:
                            return await channel.send(embed=embed)

                if before.discriminator != after.discriminator:
                    embed = discord.Embed(
                        title='Użytkownik zmienił tag <a:greenbutton:919647666101694494>',
                        color=discord.Color.from_rgb(108, 203, 3),
                        timestamp=datetime.utcnow() + timedelta(hours=1)
                    )
                    embed.add_field(name='<a:strzalka:919651065597669407> Wcześniej', value=f'`{before.discriminator}`',
                                    inline=False)
                    embed.add_field(name='<a:strzalka:919651065597669407> Aktualnie', value=f'`{after.discriminator}`',
                                    inline=False)
                    embed.add_field(name='<a:strzalka:919651065597669407> Użytkownik', value=f'`{user}`')
                    embed.set_thumbnail(url=user.avatar.url)

                    for channel in user.guild.channels:
                        if channel.id == channel_id:
                            return await channel.send(embed=embed)


def setup(client):
    client.add_cog(Event_User_Update(client))
