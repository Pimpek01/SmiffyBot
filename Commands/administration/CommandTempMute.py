import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix
from asyncio import sleep


class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm', 'h', 'd']:
            return [int(amount), unit]

        raise commands.BadArgument(message='Zła jednostka czasu')


class CommandTempmute(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def tempmute(self, ctx, member: discord.Member, duration: DurationConverter, *, reason: str = 'Brak'):
        guild = ctx.guild
        mutedrole = discord.utils.get(guild.roles, name="Zmutowany")

        for role in ctx.author.roles:
            if role == mutedrole:
                embed = discord.Embed(
                    title='<:error:919648598713573417> Wystąpił błąd.',
                    description=f'**{member}** Posiada już wyciszenie!',
                    timestamp=datetime.utcnow() + timedelta(hours=1),
                    color=discord.Color.red())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                try:
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                except AttributeError:
                    pass
                return await ctx.send(embed=embed)

        if not mutedrole:
            embed = discord.Embed(
                title='<a:loading:919653287383404586> Jeszcze Chwilka!',
                description='`Na serwerze nie zostala znaleziona rola: Zmutowany`\n`'
                            'Jestem w trakcie tworzenia, oraz ustawienia wszystkich uprawnień.`',
                color=discord.Color.red()
            )
            embed.set_footer(text='Czas oczekiwania jest zależny od ilości kanałów Na serwerze!')
            await ctx.send(embed=embed, delete_after=4)
            mutedrole = await guild.create_role(name="Zmutowany")

            for channel in guild.channels:
                await channel.set_permissions(mutedrole, speak=False, send_messages=False)

        await member.add_roles(mutedrole, reason=reason)
        amount, unit = duration
        embed = discord.Embed(
            title='Użytkownik został zmutowany <a:greenbutton:919647666101694494>',
            color=discord.Color.green(),
            timestamp=datetime.utcnow() + timedelta(hours=1)
        )
        embed.add_field(name='Administrator', value=f'`{ctx.author}`')
        embed.add_field(name='Użytkownik', value=f'`{member}`', inline=False)
        embed.add_field(name='Powód', value=f'`{reason}`', inline=True)
        embed.add_field(name='Czas', value=f'`{amount}{unit}`', inline=True)
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        await sleep(amount * self.multiplier[unit])
        await member.remove_roles(mutedrole, reason=reason)

    @tempmute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}TempMute <@member/id> <czas> <powód>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}TempMute <@member/id> <czas> <powód>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Niestety, ale nie posiadasz permisji » `Manage_Channels`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CommandTempmute(client))
