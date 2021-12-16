import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


class Command_Powiedz(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.mentions = discord.AllowedMentions(everyone=False, users=False, roles=False)

    @commands.command(aliases=['say'])
    async def powiedz(self, ctx, *, message: str):
        await ctx.reply(message, mention_author=False, allowed_mentions=self.mentions)

    @powiedz.error
    async def powiedz_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:warning:868110552268931114> Wystąpił Błąd.',
                timestamp=datetime.utcnow(),
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Powiedz <tekst>`',
                color=discord.Color.red()
            )
            embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_Powiedz(client))
