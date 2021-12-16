import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


def embed_ban(ctx):
    embed = discord.Embed(
        title='<:error:919648598713573417> Wystąpił błąd.',
        color=discord.Color.red(),
        timestamp=datetime.utcnow() + timedelta(hours=1),
        description='Nie odnaleziono tego użytkownika z blokadą'
    )
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
    try:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    except AttributeError:
        pass
    return embed


class BannedMember(commands.Converter):
    async def convert(self, ctx, argument):
        if argument.isdigit():
            member_id = int(argument, base=10)
            try:
                return await ctx.guild.fetch_ban(discord.Object(id=member_id))
            except discord.NotFound:
                return await ctx.send(embed=embed_ban(ctx))

        ban_list = await ctx.guild.bans()
        entity = discord.utils.find(lambda u: str(u.user) == argument, ban_list)

        if entity is None:
            return await ctx.send(embed=embed_ban(ctx))
        return entity


class CommandUnban(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['odbanuj'])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: BannedMember, *, reason: str = 'Brak'):
        embed = discord.Embed(
            title='Pomyślnie odbanowano <a:greenbutton:919647666101694494>',
            color=discord.Color.green(),
            timestamp=datetime.utcnow() + timedelta(hours=1)
        )
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        embed.add_field(name='Użytkownik', value=f'{member.user}')
        embed.add_field(name='Powód', value=f'{reason}', inline=False)
        await ctx.guild.unban(member.user, reason=reason)
        return await ctx.send(embed=embed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Niestety, ale nie posiadasz permisji » `Ban_Members`',
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
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Unban <@member/id> <powód>`',
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
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}Unban <@member/id> <powód>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CommandUnban(client))
