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
        if len(channels) > 5:
            await ctx.send("Can't compare more than 5 channels! (heavy traffic)")
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
    async def top(self, ctx, *channels: discord.TextChannel):
        if len(channels) > 5:
            await ctx.send("Can't compare more than 5 channels! (heavy traffic)")
        clist = list()
        lemb = core.Core.baseEmb(title = '**Loading...**', description = '')
        lemb.set_image(url = 'https://cdn.discordapp.com/attachments/842390346029727814/848682289202069584/044.gif')
        lmsg = await ctx.send(embed = lemb)
        async with ctx.typing():
            for i in channels:
                ulist = list()
                async for h in i.history(limit = 1000):
                    if h.author.bot:
                        continue
                    chc = False
                    if not ulist:
                        userdat = h.author.id, 1
                        ulist.append(userdat)
                        continue
                    for c in range(0, len(ulist)):
                        if h.author.id in ulist[c]:
                            userdat = h.author.id, ulist[c][1] + 1
                            ulist[c] = userdat
                            chc = True
                            break                          
                    if not chc:
                        userdat = h.author.id, 1
                        ulist.append(userdat)
                ulist.sort(key = lambda x: x[1], reverse= True)
                clist.append(ulist)
        emb = core.Core.baseEmb(title = 'Most sent messages', description = '')
        for i in range(0, len(channels)):
            try:
                nr1u = ctx.guild.get_member(clist[i][0][0])
                nr2u = ctx.guild.get_member(clist[i][1][0])
                nr3u = ctx.guild.get_member(clist[i][2][0])
                nr1a, nr2a, nr3a = clist[i][0][1], clist[i][1][1], clist[i][2][1]
            except IndexError:
                await ctx.send(f"Less than 3 users have sent in this channel : {channels[i].name}")
                return
            desc = f"""
            🥇 {nr1u.mention} {nr1a}\n
            🥈 {nr2u.mention} {nr2a}\n
            🥉 {nr3u.mention} {nr3a}\n"""
            emb.add_field(name = f'#{channels[i].name}', value = desc)
        await lmsg.delete()
        await ctx.send(embed = emb)

                    
def setup(bot):
    bot.add_cog(Stats(bot))