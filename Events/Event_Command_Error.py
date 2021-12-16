from nextcord.ext import commands
from datetime import datetime, timedelta
from utilities import get_prefix


class EventCommandError(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            if get_prefix(self.client, ctx) == '':
                return
        with open('Data/logs.txt', mode='a') as file:
            text = f"-- > {ctx.author}: (Error) [{error}] < --\n"
            save = file.write(text)
            file.close()


def setup(client):
    client.add_cog(EventCommandError(client))
