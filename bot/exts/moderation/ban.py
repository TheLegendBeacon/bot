import discord
from discord.ext import commands


class Ban(commands.Cog):
    """Cog for ban command."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_role("Cat Devs")
    async def ban(self, ctx: commands.Context, user: discord.User = None, reason: str = "Badly behaved"):
        if user == self.bot.user:
            await ctx.send("You can't ban me!")
            return
        elif user == ctx.author:
            await ctx.send("You can't ban yourself!")
            return
        await ctx.send(f"Succesfully banned {user.name}")
        await ctx.guild.ban(user)


def setup(bot: commands.Bot):
    """Loads cog."""
    bot.add_cog(Ban(bot))


