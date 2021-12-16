import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm', 'h', 'd']:
            return [int(amount), unit]

        raise commands.BadArgument(message='Zła jednostka czasu')


class Command_Slowmode(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.multiplier = {'s': 1, 'm': 60, 'h': 3600}

    @commands.command(aliases=['cooldown'])
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, time: DurationConverter):
        amount, unit = time
        try:
            await ctx.channel.edit(slowmode_delay=amount * self.multiplier[unit])
            embed = discord.Embed(
                title='Poprawnie zaktualizowano slowmode!',
                color=discord.Color.light_gray()
            )
            message = await ctx.send(embed=embed)
            emotka = self.client.get_emoji(863961893998821386)
            await message.add_reaction(emotka)
        except:
            embed = discord.Embed(
                title='Wystąpił nieoczekiwany błąd!',
                description='Podczas wykonywania komendy wystąpił błąd sprawdź czy',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red()
            )
            embed.add_field(name='Nie przekroczyłeś dozwolnego limitu:', value='Maksymalny czas: 6h')
            embed.add_field(name='Podales poprawna jednostke:', value='**1s**, **1m**, **1h**', inline=False)
            await ctx.send(embed=embed)

    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title='Wystąpił nieoczekiwany błąd!',
                description='Podczas wykonywania komendy wystąpił błąd sprawdź czy:',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red()
            )
            embed.add_field(name='Nie przekroczyłeś dozwolnego limitu:', value='Maksymalny czas: 6h')
            embed.add_field(name='Podales poprawna jednostke:', value='**1s**, **1m**, **1h**', inline=False)
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}slowmode <czas>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red()
            )
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='<<:error:919648598713573417> Wystąpił błąd.',
                description=f'Niestety, ale nie posiadasz permisji » `Manage Channels`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red()
            )
            embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Command_Slowmode(client))
