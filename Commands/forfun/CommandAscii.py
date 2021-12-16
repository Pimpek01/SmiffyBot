from pyfiglet import Figlet
import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
import nextcord


class CommandAscii(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['figlet'])
    async def ascii(self, ctx, *, message):
        if len(message) > 10:
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił Błąd.',
                timestamp=datetime.utcnow() + timedelta(hours=2),
                color=discord.Color.red(),
                description='Tekst Nie Może Przekraczać **10** liter!'
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)
        f = Figlet(font='slant')
        return await ctx.send(f"```{f.renderText(message)}```")


def setup(client):
    client.add_cog(CommandAscii(client))
