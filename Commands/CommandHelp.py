import nextcord as discord
from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


class CommandHelpButtons(discord.ui.View):

    def __init__(self, ctx, **kwargs):
        super().__init__()
        self.ctx = ctx

        self.embed = discord.Embed(
            title='Spis wszystkich komend',
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow() + timedelta(hours=1)
        )
        self.embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)

    async def interaction_check(self, interaction):
        res = self.ctx.author == interaction.user
        if res:
            return res
        return await interaction.response.send_message('Nie możesz użyć, nie swojej komendy.', ephemeral=True)

    @discord.ui.button(label='Administracyjne', style=discord.ButtonStyle.red)
    async def administracyjne(self, button: discord.ui.Button, interaction: discord.Interaction):
        ctx = interaction.message
        self.embed.description = 'Kategoria: **Administracyjne**\n\n' \
                                     '`Ban`, `Tempban`, `Unban`, `Kick`, `Mute`, `Tempmute`,' \
                                     '`Unmute`, `Warn`, `Unwarn`, `Warnings` `Slowmode`, `Clear`, `Dodajrole`, `DodajEmoji`'
        try:
            self.embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(label='Ustawienia', style=discord.ButtonStyle.blurple)
    async def ustawienia(self, button: discord.ui.Button, interaction: discord.Interaction):
        ctx = interaction.message
        self.embed.description = 'Kategoria: **Ustawienia**\n\n' \
                                 '`Prefix`, `Startowarola`, `AntyLink`, `Logi`'
        try:
            self.embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(label='Dodatkowe', style=discord.ButtonStyle.blurple)
    async def dodatkowe(self, button: discord.ui.Button, interaction: discord.Interaction):
        ctx = interaction.message
        self.embed.description = 'Kategoria: **Dodatkowe**\n\n' \
                                 '`Ping`, `Avatar`, `SerwerInfo`, `Userinfo`, `Ankieta`, `Zglosblad`'
        try:
            self.embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        await interaction.response.edit_message(embed=self.embed)

    @discord.ui.button(label='ForFun', style=discord.ButtonStyle.blurple)
    async def forfun(self, button: discord.ui.Button, interaction: discord.Interaction):
        ctx = interaction.message
        self.embed.description = 'Kategoria: **ForFun**\n\n' \
                                 '`Ascii`, `Pytanie`, `Powiedz`, `Meme`, `Pies`, `Kot`, `Panda`, `Captcha`, `Google`, ' \
                                 '`Trump`, `Darken`, `Coinflip`'
        try:
            self.embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        await interaction.response.edit_message(embed=self.embed)


class CommandHelp(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        prefix = get_prefix(self.client, ctx)
        if prefix == '':
            prefix = 'Invisible!'
        b = CommandHelpButtons(ctx=ctx)
        embed = discord.Embed(
            title='Spis wszystkich komend',
            color=discord.Color.dark_theme(),
            description=f'Aktualny prefix: `{prefix}`\n'
                        f'Liczba wszystkich komendy: `36`',
            timestamp=datetime.utcnow() + timedelta(hours=1)
        )
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        try:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        except AttributeError:
            pass
        await ctx.send(embed=embed, view=b)
        await b.wait()


def setup(client):
    client.add_cog(CommandHelp(client))
