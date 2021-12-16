from nextcord import Intents, Game
from nextcord.ext import commands
from utilities import *

client = commands.Bot(command_prefix=get_prefix, intents=Intents.all(), case_insensitive=True)
client.remove_command('help')


@client.event
async def on_ready():
    register_login_to_logs()
    load_cogs(client)
    print(welcome_messsage())
    await client.change_presence(activity=Game(f"Serwery: {len(client.guilds)}"))


client.run(get_token())
