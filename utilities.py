from itertools import cycle
from json import load
from nextcord import Game
from nextcord.ext import commands, tasks
from datetime import datetime, timedelta
from os import listdir
import sqlite3


def get_token() -> str:

    with open('Data/config.json', mode='r') as file:
        token = load(file)

        if token['TOKEN'] != '':
            return token['TOKEN']

        print('Nie udało się uruchomić bota, wpisz token w Data/config.json')
        exit()


def get_prefix(client, ctx: commands.Context):

    global prefix
    db = sqlite3.connect('Data/smiffy_base.db')
    c = db.cursor()
    c.execute(f'SELECT prefix FROM prefixes WHERE guild_id = {ctx.guild.id}')
    res = c.fetchone()

    if res:
        prefix = str(res[0])
    if not res:
        prefix = 's!'
    db.commit()
    c.close()
    db.close()

    return prefix


def welcome_messsage() -> str:

    return """
Smiffy został poprawnie uruchommiony
"""


def register_login_to_logs():

    with open('Data/logs.txt', mode='w') as file:
        file.write(f'-- > Bot launched [{str(datetime.utcnow() + timedelta(hours=1))[:19]}] < --\n')
        file.close()


def load_cogs(client):

    with open('Data/logs.txt', mode='a') as f:

        for file in listdir('./Events'):
            if file.endswith('.py'):
                client.load_extension(f'Events.{file[:-3]}')
                f.write(f"-- > Extension: ({file[:-3]}) Successfully Loaded < --\n")

        for folder in listdir(f'./Commands'):
            if folder.endswith('.py'):
                client.load_extension(f'Commands.{folder[:-3]}')
                continue
            for file in listdir(f'./Commands/{folder}'):
                if file.endswith('.py'):
                    client.load_extension(f'Commands.{folder}.{file[:-3]}')
                    f.write(f"-- > Extension: ({file[:-3]}) Successfully Loaded < --\n")

        f.close()


