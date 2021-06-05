import discord
from discord import utils
from discord.ext import commands

def getuser(guild, user):
    if isinstance(user, list):
        m = ' '.join(user)
    else:
        m = user
    try:
        if int(m):
            member = guild.get_member(int(m))
            if not member:
                pass
            else:
                return member
    except ValueError:
        pass
    if  m.startswith('<@!'):
        m = m.lstrip('<@!')
        m = m.rstrip('>')
        member = utils.get(guild.members, id = int(m))
        if not member:
            raise commands.BadArgument
        else:
            return member
    else:
        for i in guild.members:
            if i.name.lower().startswith(m):
                member = i
                break
            elif i.nick:
                if i.nick.lower().startswith(m):
                    member = i
                    break
            else:
                member = None
        if not member:
            raise commands.BadArgument
        else:
            return member

def getusers(guild, users):
    mlist = list()
    for i in users:
        member = getuser(guild, i)
        mlist.append(member)
    return mlist