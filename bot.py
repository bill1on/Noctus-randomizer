import discord
from discord import activity
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix= 'n!', intents = intents, activity = activity.CustomActivity(name = "hi"))
extensions = ['cogs.core', 'cogs.errorhandle', 'cogs.stat', 'cogs.mod']


@client.event
async def on_ready():
    print('Ready!')

if __name__ == '__main__':
    for extension in extensions:
        client.load_extension(extension)
    with open('token.txt', 'r') as f:
        token = f.read()
        client.run(token)