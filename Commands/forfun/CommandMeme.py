import nextcord as discord
from nextcord.ext import commands
from requests import get
from datetime import datetime, timedelta


class CommandMeme(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['mem'])
    async def meme(self, ctx):
        r = get('https://ivall.pl/memy')
        json_data = r.json()
        image_url = json_data['url']
        embed = discord.Embed(
            title='O To Twój Mem!',
            timestamp=datetime.utcnow() + timedelta(hours=1),
            color=discord.Color.blurple()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CommandMeme(client))