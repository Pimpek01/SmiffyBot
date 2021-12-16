import nextcord as discord
from nextcord.ext import commands
from io import BytesIO
from aiohttp import ClientSession
from datetime import datetime, timedelta
from utilities import get_prefix


class CommandCaptcha(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def captcha(self, ctx, *, tekst: str):
        async with ClientSession() as session:
            async with session.get(f'https://api.no-api-key.com/api/v2/recaptcha?text={tekst}') as resp:
                if resp.status != 200:
                    return
                data = BytesIO(await resp.read())
                await ctx.channel.send(file=discord.File(data, 'cool_image.png'))

    @captcha.error
    async def captcha_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił Błąd.',
                description=f'Poprawne Uzycie » `{get_prefix(self.client, ctx)}Captcha <tekst>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red()
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CommandCaptcha(client))
