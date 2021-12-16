import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from requests import get


class CommandAnimals(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['dog'])
    async def pies(self, ctx):
        r = get('https://no-api-key.com/api/v2/animals/dog')
        json_data = r.json()
        image_url = json_data['image']
        embed = discord.Embed(
            timestamp=datetime.utcnow() + timedelta(hours=1),
            color=discord.Color.from_rgb(255, 133, 128)
        )
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cat'])
    async def kot(self, ctx):
        r = get('https://no-api-key.com/api/v2/animals/cat')
        json_data = r.json()
        image_url = json_data['image']
        embed = discord.Embed(
            timestamp=datetime.utcnow() + timedelta(hours=1),
            color=discord.Color.from_rgb(255, 133, 128)
        )
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def panda(self, ctx):
        r = get('https://no-api-key.com/api/v2/animals/panda')
        json_data = r.json()
        image_url = json_data['image']
        embed = discord.Embed(
            timestamp=datetime.utcnow() + timedelta(hours=1),
            color=discord.Color.from_rgb(255, 133, 128)
        )
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CommandAnimals(client))
