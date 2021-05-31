import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix= 'n!', intents = intents)
extensions = ['cogs.core', 'cogs.errorhandle']


@client.event
async def on_ready():
    print('Ready!')

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except:
            print("Couldn't load %s", extension)
    with open('token.txt', 'r') as f:
        token = f.read()
        client.run(token)