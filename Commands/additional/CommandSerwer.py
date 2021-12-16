import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta


class Command_Serwer(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['serwerinfo', 'server', 'serverinfo'])
    async def serwer(self, ctx):
        guild = str(ctx.guild.created_at)

        embed = discord.Embed(
            title=f'Informacje o serwerze: {ctx.guild}',
            description=f'''
👑 • Założyciel: **{ctx.guild.owner.name}**
━━
📃 • Nazwa serwera: **{ctx.guild.name}**
━━
:id: • Serwer ID: **{ctx.guild.id}**
━━
🗓️ • Stworzony: **{guild[0: 16]}**
━━
<a:nitro:919655460905320448> • Boosty: **{ctx.guild.premium_subscription_count}**
━━
👥 • Osoby: **{sum(not member.bot for member in ctx.guild.members)}**
━━
👾 • Boty: **{sum(member.bot for member in ctx.guild.members)}**
━━
📋 • Kanały: **{len(ctx.guild.text_channels + ctx.guild.voice_channels)}**
━━
🎫 • Role: **{len(ctx.guild.roles) -1}**
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
    client.add_cog(Command_Serwer(client))
