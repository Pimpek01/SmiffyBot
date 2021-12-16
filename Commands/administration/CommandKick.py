import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


class CommandKick(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['wyrzuc'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = 'Brak'):
        if ctx.guild.me.top_role <= member.top_role:
            error_embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'**Niestety, ale nie mam wystarczających uprawnień, aby wyrzucić: **`{member}`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            error_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                error_embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=error_embed)
        if ctx.author.top_role > member.top_role and member != ctx.guild.owner:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title='Pomyślnie wyrzucono <a:greenbutton:919647666101694494>',
                color=discord.Color.green(),
                timestamp=datetime.utcnow() + timedelta(hours=1)
                )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            embed.add_field(name='Użytkownik', value=f'<a:bialastrzalka:919651308124921936> `{member}`')
            embed.add_field(name='Powód', value=f'<a:bialastrzalka:919651308124921936> `{reason}`')
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)
        else:
            error_embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'**Niestety, ale `{ctx.author}` nie możesz wyrzucić: `{member}`**',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            error_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                error_embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=error_embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Niestety, ale nie posiadasz permisji » `Kick_Members`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}kick <@member> <powód>`',
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
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}kick <@member> <powód>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CommandKick(client))
