import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta


class CommandSerwer(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['serwerinfo', 'server', 'serverinfo'])
    async def serwer(self, ctx):
        guild = str(ctx.guild.created_at)

        embed = discord.Embed(
            title=f'Informacje o serwerze: {ctx.guild}',
            description=f'''
π β’ ZaΕoΕΌyciel: **{ctx.guild.owner.name}**
ββ
π β’ Nazwa serwera: **{ctx.guild.name}**
ββ
:id: β’ Serwer ID: **{ctx.guild.id}**
ββ
ποΈ β’ Stworzony: **{guild[0: 16]}**
ββ
<a:nitro:919655460905320448> β’ Boosty: **{ctx.guild.premium_subscription_count}**
ββ
π₯ β’ Osoby: **{sum(not member.bot for member in ctx.guild.members)}**
ββ
πΎ β’ Boty: **{sum(member.bot for member in ctx.guild.members)}**
ββ
π β’ KanaΕy: **{len(ctx.guild.text_channels + ctx.guild.voice_channels)}**
ββ
π« β’ Role: **{len(ctx.guild.roles) -1}**
''',
            color=discord.Color.from_rgb(123, 191, 233),
            timestamp=datetime.utcnow() + timedelta(hours=1)
        )
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CommandSerwer(client))
