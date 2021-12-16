import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


class Command_Google_Buttons(discord.ui.View):

    def __init__(self, query):
        super().__init__()

        q = query.replace(' ', '+')
        query = f'https://letmegooglethat.com/?q={q}'
        self.add_item(discord.ui.Button(label='Wynik Wyszukiwania', url=query))


class Command_Google(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def google(self, ctx, *, query: str):
        embed = discord.Embed(
            title='Komenda google',
            color=discord.Color.green(),
            timestamp=datetime.utcnow() + timedelta(hours=1)
        )
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed, view=Command_Google_Buttons(query))

    @google.error
    async def google_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Google <Tekst>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_Google(client))