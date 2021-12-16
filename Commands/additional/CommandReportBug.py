import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


class Command_ReportBug(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.report_channel: int = 919642661248462890

    @commands.command()
    async def zglosblad(self, ctx, *, blad: str):
        channel = self.client.get_channel(self.report_channel)
        member = ctx.author
        guild = ctx.guild

        embed = discord.Embed(
            title='Zgłoszono błąd <a:redalert:919657291639320696>',
            color=discord.Color.red(),
            timestamp=datetime.utcnow() + timedelta(hours=1)
        )
        embed.add_field(name='Zgłaszający', value=f'{member} \n(`{member.id}`)')
        embed.add_field(name='Serwer', value=f'{guild} \n(`{guild.id}`)')
        embed.add_field(name='Treść Błedu', value=f'```{blad}```', inline=False)
        await channel.send(embed=embed)

        reply_embed = discord.Embed(
            title='Pomyślnie zgłoszono błąd <a:greenbutton:919647666101694494>',
            description='Błąd został wysłany do administratorów.\nPamiętaj, aby nie używać tej komendy bezcelowo!',
            color=discord.Color.green(),
            timestamp=datetime.utcnow() + timedelta(hours=1)
        )
        try:
            reply_embed.set_thumbnail(url=ctx.author.avatar.url)
        except AttributeError:
            pass
        await ctx.reply(embed=reply_embed)

    @zglosblad.error
    async def zglosblad_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Zglosblad <opis błędu>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_ReportBug(client))
