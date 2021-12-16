import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from time import time
from utilities import get_prefix


class Event_Mentions_Buttons(discord.ui.View):

    def __init__(self):
        super().__init__()

        discord_url = 'https://discord.gg/NTHJPenwug'
        bot_invite_url = 'https://discord.com/api/oauth2/authorize?client_id=911240424813891614&permissions=8&scope=bot'
        self.add_item(discord.ui.Button(label='Discord Support', url=discord_url))
        self.add_item(discord.ui.Button(label='Zaproszenie', url=bot_invite_url))


class EventMentionBot(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.start_bot_time = time()

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.mentioned_in(message):
            if message != '@everyone' and message.content[1] == '@':
                prefix = get_prefix(self.client, message)
                if prefix == '':
                    prefix = 'Invisible!'

                current_time = time()
                uptime = int(round(current_time - self.start_bot_time))
                text = str(timedelta(seconds=uptime))
                embed = discord.Embed(
                    title='Oho, Ktoś mnie wezwał!',
                    color=discord.Color.from_rgb(180, 217, 192),
                    timestamp=datetime.utcnow() + timedelta(hours=2),
                    description=f'*Skoro już mnie wezwałeś/aś pozwól, że ci się przedstawię. Nazywam się Smiffy jestem tutaj, żeby ci pomóc. '
                                f'Moje komendy możesz sprawdzić komendą: **{get_prefix(self.client, message)}help**\n'
                                f'Na dole możesz zobaczyć przydatne informacje na mój temat.*'
                )
                embed.add_field(name='Serwerowy Prefix ⚙️', value=f'`{prefix}`')
                embed.add_field(name='UpTime ⏱', value=f'`{text}`')
                embed.add_field(name='Autor :bust_in_silhouette:', value=f'`Pimpek01#5529`')
                embed.set_author(name=message.author, icon_url=message.author.avatar.url)
                await message.channel.send(embed=embed, view=Event_Mentions_Buttons())


def setup(client):
    client.add_cog(EventMentionBot(client))
