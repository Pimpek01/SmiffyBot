from nextcord.ext import commands
import nextcord as discord
from random import choice


class Command_CoinFlip(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def coinflip(self, ctx):
        embed = discord.Embed(
            title='Rzut moneta',
            color=discord.Color.green()
        )
        result = choice(
            ['https://no-api-key.com/image/quarter/tails.gif', 'https://no-api-key.com/image/quarter/heads.gif'])
        embed.set_image(url=result)
        await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Command_CoinFlip(client))