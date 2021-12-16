import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta


class CommandAvatar(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):

        if not member:
            member = ctx.author
        embed = discord.Embed(
            title=f'Avatar: {member}',
            description=f'[Link]({member.avatar.url})',
            color=discord.Color.dark_theme(),
            timestamp=datetime.utcnow()
        )
        embed.set_image(url=member.avatar.url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CommandAvatar(client))
