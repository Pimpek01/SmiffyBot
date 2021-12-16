import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from nextcord.utils import get


class Command_User(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['userinfo'])
    async def user(self, ctx, member: discord.Member = None):
        user = ctx.author
        top_role = ctx.author.top_role
        if member:
            top_role = member.top_role
            user = member

        created = str(user.created_at)
        joined = str(user.joined_at)
        embed = discord.Embed(
            title=f'Informacje użytkownika',
            color=discord.Color.blue(),
            timestamp=datetime.utcnow() + timedelta(hours=1),
            description=f'''
:bust_in_silhouette: • Nick: **{user}**

:id: • ID: **{user.id}**

🧾 • Ważność Konta: **{created[0: 16]}**

<:PurplePlus:919656968451391529> • Dołączył: **{joined[0: 16]}**

<:PurpleRole:919657090178506793> • Najwyższa rola: **{top_role}**
'''
        )
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_User(client))