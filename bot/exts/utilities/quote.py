from discord.ext import commands
import discord

from bot.utilities import get_yaml_val

quotechannel = get_yaml_val("bot/config.yml", 'guild')['guild']["channels"]["quotes"]


class Quote(commands.Cog):
    """Cog for the quote command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("quote", aliases=["q"])
    @commands.has_any_role(833841708805652481, 852267769985761281, 839844083463749664)
    async def quote(self, ctx: commands.Context, user: discord.User, *, quote: str):
        """Quotes a user on a sent message."""
        channel = self.bot.get_channel(quotechannel)
        await channel.send(f"{user.mention}: {quote}")
        await ctx.send("Successfully quoted message.")


def setup(bot: commands.Bot):
    """Loads the quote cog."""
    bot.add_cog(Quote(bot))
