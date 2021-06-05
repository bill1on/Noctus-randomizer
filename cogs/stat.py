import discord
from discord.ext import commands
import matplotlib.pyplot as plt
from cogs import core
from tools import usrt

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def getdat(ctx, channels):
        cdat = list()
        async with ctx.typing():
            for i in channels:
                c = 0
                async for x in i.history(limit = None):
                    c += 1
                cdat.append(c)
        print(cdat)
        return cdat

    @commands.group(invoke_without_command = True)
    async def stat(self, ctx):
        emb = core.Core.baseEmb(title = 'Channel stats', description = 'Statistics manager for channels.')
        emb.add_field(name = 'Compare messages sent:', value = '`n!stat channel <channel1> *<channel2> ...`', inline = False)
        emb.add_field(name = 'Get most messages sent in channel:', value = '`n!stat top <channel1> *<channel2> ...`', inline = False)
        await ctx.send(embed = emb)

    @stat.command()
    async def channel(self, ctx, *channels: discord.TextChannel):
        cname = list()
        emb = core.Core.baseEmb(title = '**Loading...**', description = '')
        emb.set_image(url = 'https://cdn.discordapp.com/attachments/842390346029727814/848682289202069584/044.gif')
        lmsg = await ctx.send(embed = emb)
        cdat = await self.getdat(ctx, channels)
        for i in channels:
            cname.append(i.name)
        plt.bar(cname, cdat)
        plt.xlabel("Groups")
        plt.ylabel("Total messages sent")
        plt.savefig('dats/dat.png')
        dat = discord.File('dats/dat.png')
        await lmsg.delete()
        await ctx.send(file = dat)

    @stat.command()
    async def user(self, ctx, *users):
        mlist = usrt.getusers(ctx.guild, users)
        for i in mlist:
            await ctx.send(i.name)



def setup(bot):
    bot.add_cog(Stats(bot))