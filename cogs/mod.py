import discord
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.check_any(commands.has_permissions(administrator = True), commands.is_owner())
    @commands.command()
    async def purge(self, ctx, channel: discord.TextChannel, *word):
        msg = await ctx.send("Deleting...")
        async with ctx.typing():
            async for i in channel.history(limit = None):
                for x in word:
                    if i.lower() == x.lower():
                        await i.delete()
        await msg.delete()
        await ctx.send("Deleted.")

def setup(bot):
    bot.add_cog(Mod(bot))