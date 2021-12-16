from nextcord.ext.commands import command, Cog


class Command_Ping(Cog):

    def __init__(self, client):
        self.client = client

    @command()
    async def ping(self, ctx):
        latecy = round(self.client.latency * 1000)

        message = await ctx.send('Pong!')
        await message.edit(f'Pong! {latecy}ms')


def setup(client):
    client.add_cog(Command_Ping(client))