import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix
from dotenv import load_dotenv
import aiohttp
from io import BytesIO


class CommandDodajEmoji(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['createmoji', 'stworzemoji'])
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def dodajemoji(self, ctx, url: str, *, name):
        load_dotenv()
        guild = ctx.guild
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    img_or_gif = BytesIO(await r.read())
                    b_value = img_or_gif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=b_value, name=name)
                        if r.headers['content-type'] == "image/gif":
                            emoji = f'<a:{name}:{emoji.id}>'
                        else:
                            emoji = f'<:{name}:{emoji.id}>'
                            embed = discord.Embed(
                                title=f'Pomyślnie dodano emoji <a:greenbutton:919647666101694494>',
                                color=discord.Color.from_rgb(100, 235, 32),
                                timestamp=datetime.utcnow() + timedelta(hours=1)
                            )
                            try:
                                embed.set_thumbnail(url=ctx.guild.icon.url)
                            except AttributeError:
                                pass
                            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)

                            await ctx.send(embed=embed)
                            await ses.close()
                    else:
                        await ctx.send(f'Nie udało się dodać emotki kod błędu: | {r.status}')
                        await ses.close()

                except discord.HTTPException:
                    await ctx.send(f'Nie udało się dodać emotki kod błędu: | {r.status}')

    @dodajemoji.error
    async def dodajemoji_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title='<:error:919648598713573417> Wystąpił błąd.',
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}dodajEmoji <link> <nazwa>`',
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
                description=f'Poprawne użycie: `{get_prefix(self.client, ctx)}dodajemoji <link> <nazwa>`',
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
                description=f'Niestety, ale nie posiadasz permisji » `Manage_emojis_and_stickers`',
                timestamp=datetime.utcnow() + timedelta(hours=1),
                color=discord.Color.red())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
            try:
                embed.set_thumbnail(url=ctx.guild.icon.url)
            except AttributeError:
                pass
            return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(CommandDodajEmoji(client))
