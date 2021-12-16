import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


class CommandUnmute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['odmutuj'])
    @commands.has_permissions(manage_channels=True)
    async def unmute(self, ctx, member: discord.Member):

        mutedrole = discord.utils.get(ctx.guild.roles, name="Zmutowany")

        for role in member.roles:
            if role == mutedrole:
                await member.remove_roles(mutedrole)
                embed = discord.Embed(
                    title='Użytkownik został odciszony <a:greenbutton:919647666101694494>',
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow() + timedelta(hours=1)
                )
                embed.add_field(name='Administrator', value=f'`{ctx.author}`')
                embed.add_field(name='Użytkownik', value=f'`{member}`', inline=False)
                try:
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                except AttributeError:
                    pass
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                return await ctx.send(embed=embed)

        embed = discord.Embed(
            title='<:error:919648598713573417> Wystąpił błąd.',
            description=f'**{member}** Nie posiada wyciszenia!',
            timestamp=datetime.utcnow() + timedelta(hours=1),
            color=discord.Color.red())
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        return await ctx.send(embed=embed)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Unmute <@member/id>`',
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
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Unmute <@member/id>`',
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
    client.add_cog(CommandUnmute(client))
