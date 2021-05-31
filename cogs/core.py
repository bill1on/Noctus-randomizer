import discord
from discord.ext import commands    
import asyncio
import datetime
import time
import random
import itertools

class Core(commands.Cog):
    emlist = ['<a:ani1:848589054866227230>', '<a:ani:848590642678333440>', '<a:ani3:848589054592155729>']
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def baseEmb(**kwargs):
        emb = discord.Embed(title = kwargs['title'], description=kwargs['description'], colour = int(0x4F27A1))
        emb.set_footer(text = f'Coded with love by:\nbillion#2126', icon_url = 'https://cdn.discordapp.com/avatars/147840568897044480/6c48b17182310a55565bb88791134d36.png')
        emb.set_author(name='Randomizer | Noctus exclusive', icon_url='https://cdn.discordapp.com/attachments/842390346029727814/848566530446327838/a_54f9085a310256206cb22393285bebca.png')
        return emb

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def get(self, ctx, *roles):
        if len(roles) > 8:
            embed = self.baseEmb(title='Error!', description = "Can't fetch over **8** roles! Please try again!")
            await ctx.send(embed=embed)
        rolelist = []
        for i in roles:
            if isinstance(i, discord.Role):
                role = i
            else:
                role = discord.utils.get(ctx.guild.roles, name=f'{i}')
                if role == None:
                    await ctx.send(f"{i} is an invalid role!")
                    return                                                   # --- MAKE EMBED
            rolelist.append(role)
# ------------------------------------------- ^^^^^^^^^^ work with ROLES
        desc = f"""**Nice**!\n
        Press the `first` button to shuffle using `previous selected roles`
        Press the `second` button to give the users `new random role(s) | WIP`
        Press the `third` button to `exit`."""
        embed = self.baseEmb(title='Got roles', description = desc)
        embed.add_field(name = '**Fetched a total of :**', value = f'**{len(rolelist)}** roles!')
        rrlist = ''
        for i in rolelist:
            rrlist = rrlist + f"**{i.name}**\n"
        embed.add_field(name="**Fetched roles:**", value = rrlist)
# ------------------------------------------- ^^^^^^^ set up EMBED
        msg = await ctx.send(embed = embed)
        for i in self.emlist:
            await msg.add_reaction(i)
            await asyncio.sleep(0.01)
        def rcheck(reaction, user):
            return reaction.message == msg and user == ctx.author and str(reaction.emoji) in self.emlist
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=rcheck)
        except asyncio.TimeoutError:
            erembed = self.baseEmb(title = '**Error!**', description = 'Timed out!')
            await ctx.send(embed = erembed, delete_after = 5.0)
            return
# ------------------------------------------ ^ add reactions and get reaction
        def splitlist(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
            
        if str(reaction) == self.emlist[2]:
            await msg.delete()
            await ctx.send("Exited!", delete_after = 3)
        elif str(reaction) == self.emlist[0]:
            ctm = time.time()
            mlist = list()
            loademb = self.baseEmb(title = '**Loading...**', description = "Please be patient...")
            loademb.set_image(url = 'https://cdn.discordapp.com/attachments/842390346029727814/848682289202069584/044.gif')
            lmsg = await ctx.send(embed = loademb)
            async with ctx.typing():
                loademb = self.baseEmb(title = '**Loading...', description = "Removing roles from users...")
                await lmsg.edit(embed = loademb)
                for i in rolelist:
                    for x in ctx.guild.members:
                        if i in x.roles:
                            await x.remove_roles(i)
                            if not x in mlist:
                                mlist.append(x)
                random.shuffle(mlist)
                slist = list()
                while not len(mlist) % len(rolelist) == 0:
                    m = mlist.pop(len(mlist)-1)
                    slist.append(m)
                num = len(mlist) / len(rolelist)
                c = 0 
                for m in splitlist(mlist, int(num)):
                    for i in m:
                        await i.add_roles(rolelist[c])
                    c += 1
                c = 0
                if not len(slist) == 0:
                    for l in slist:
                        await l.add_roles(rolelist[c])
                        c += 1
            await lmsg.delete()
        doneEmb = self.baseEmb(title = '**Done!**', description = f'**Done in:**\n**{round(time.time() - ctm, 2)}** seconds!')
        doneEmb.set_image(url = 'https://cdn.discordapp.com/attachments/842390346029727814/848681684265336872/checksecondary61.gif')
        await ctx.send(embed = doneEmb)
                    


def setup(bot):
    bot.add_cog(Core(bot))