import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


class CommandMute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = 'Brak'):
        guild = ctx.guild
        mutedrole = discord.utils.get(guild.roles, name="Zmutowany")

        for role in ctx.author.roles:
            if role == mutedrole:
                embed = discord.Embed(
                    title='<:warning:868110552268931114> Wystąpił błąd.',
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
                description='`Na serwerze nie została znaleziona rola: Zmutowany`\n`'
                            'Jestem w trakcie tworzenia, oraz ustawienia wszystkich uprawnień.`',
                color=discord.Color.red()
            )
            embed.set_footer(text='Czas oczekiwania jest zależny od ilości kanałów na serwerze!')
            await ctx.send(embed=embed, delete_after=4)
            mutedrole = await guild.create_role(name="Zmutowany")

            for channel in guild.channels:
                await channel.set_permissions(mutedrole, speak=False, send_messages=False)

        await member.add_roles(mutedrole, reason=reason)
        embed = discord.Embed(
            title='Użytkownik został zmutowany <a:greenbutton:919647666101694494>',
            color=discord.Color.green(),
            timestamp=datetime.utcnow() + timedelta(hours=1)
        )
        embed.add_field(name='Administrator', value=f'`{ctx.author}`')
        embed.add_field(name='Użytkownik', value=f'`{member}`', inline=False)
        embed.add_field(name='Powód', value=f'`{reason}`', inline=False)
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Mute <@member/id> <powód>`',
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
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Mute <@member/id> <powód>`',
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
    client.add_cog(CommandMute(client))
