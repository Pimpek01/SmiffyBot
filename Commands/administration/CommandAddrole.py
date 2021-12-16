import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


class CommandDodajRole(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['addrole', 'dodajrange'])
    @commands.has_permissions(manage_roles=True)
    async def dodajrole(self, ctx, member: discord.Member, *, role):
        roles = str(role).split(' ')
        for r in roles:
            if r.isdigit():
                add_role = ctx.guild.get_role(int(r))
            else:
                add_role = r.replace('<', '').replace('@&', '').replace('>', '')
                try:
                    add_role = ctx.guild.get_role(int(add_role))
                except:
                    embed = discord.Embed(
                        title='<:error:919648598713573417> Wystąpił błąd.',
                        description=f'`Nie odnaleziono takiej roli!`',
                        timestamp=datetime.utcnow() + timedelta(hours=1),
                        color=discord.Color.red())
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                    try:
                        embed.set_thumbnail(url=ctx.guild.icon.url)
                    except AttributeError:
                        pass
                    return await ctx.send(embed=embed)

            await member.add_roles(add_role)
        embed = discord.Embed(
            title='Pomyślnie nadano role <a:greenbutton:919647666101694494>',
            color=discord.Color.dark_teal(),
            timestamp=datetime.utcnow() + timedelta(hours=1),
            description=f'**Użytkownik:** `{member}`'
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        await ctx.send(embed=embed)

    @dodajrole.error
    async def dodajrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Niestety, ale nie posiadasz permisji » `Manage_Roles`',
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
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}dodajrole <@member/id> <@role/id>`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)

        if isinstance(error, commands.BadArgument):
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    title='<:error:919648598713573417> Wystąpił błąd.',
                    description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}dodajrole <@member/id> <@role/id>`',
                    timestamp=datetime.utcnow() + timedelta(hours=1),
                    color=discord.Color.red())
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                try:
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                except AttributeError:
                    pass
                return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CommandDodajRole(client))