import nextcord as discord
from nextcord.ext import commands
from io import BytesIO
from aiohttp import ClientSession


class CommandDarken(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['dark'])
    async def darken(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        async with ClientSession() as session:
            async with session.get(f'https://api.no-api-key.com/api/v2/darken?image={member.avatar.url}') as resp:
                if resp.status != 200:
                    return
                data = BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, 'cool_image.png'))


def setup(client):
    client.add_cog(CommandDarken(client))
