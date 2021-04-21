from discord.ext import commands


class PurgeThemAll(commands.Cog):
    """Cog for purge command"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    
    @commands.command(aliases=["yeetmsg"])
    @commands.has_role("Cat Devs")
    async def purge(self, ctx: commands.Context, limit: str) -> None:
        if not 0 < int(limit) < 200:
            await ctx.send("Please purge between 0 and 200 messages.")
            return
        
        await ctx.channel.purge(limit=int(limit))
        await ctx.send(f"{ctx.message.author.mention} purged at most {limit} messages.")

        
def setup(bot: commands.Bot) -> None:
    """Loads the purge cog."""
    bot.add_cog(PurgeThemAll(bot))
