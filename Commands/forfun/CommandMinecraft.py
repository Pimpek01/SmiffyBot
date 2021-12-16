import nextcord as discord
from nextcord.ext import commands
from requests import get
from datetime import datetime, timedelta


def getinfo(serwer):

    request = get(url=serwer)
    result = request.json()
    if result['ip'] == '127.0.0.1':
        return None

    return result



class Command_Minecraft(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.API = 'https://api.mcsrvstat.us/2/'

    @commands.command()
    async def minecraft(self, ctx, serwer: str):
        info = getinfo(self.API + serwer)
        if info:
            ip = info['ip']
            port = info['port']
            online = info['online']
            players = info['players']['online']
            max_players = info['players']['max']
            embed = discord.Embed(
                title='Informacje o serwerze minecraft',
                color=discord.Color.dark_green(),
                description=f'''```
IP: {ip}
Port: {port}
Serwer Online: {online}
Players: {players}/{max_players}
```''',
                timestamp=datetime.utcnow() + timedelta(hours=1)
                )
            await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Command_Minecraft(client))