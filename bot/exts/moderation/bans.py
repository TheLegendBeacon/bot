import asyncio
import discord
from discord.ext import commands

from bot.constants import Channels


class Moderation(commands.Cog):
    """Cog for moderation commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Cat Devs")
    async def pban(
        self,
        ctx: commands.Context,
        user: discord.User = None,
        *,
        reason: str = "Badly behaved",
    ):
        if user == self.bot.user:
            await ctx.send("You can't ban me!")
            return
        elif user == ctx.author:
            await ctx.send("You can't ban yourself!")
            return
        await ctx.send(f"Succesfully banned {user.name}")
        channel = self.bot.get_channel(Channels.modlog)
        await channel.send(
            f"`{ctx.author.mention}` banned `{user.mention}` for reason `{reason}`."
        )
        await ctx.guild.ban(user)

    @commands.command()
    @commands.has_role("Cat Devs")
    async def mute(
        self,
        ctx: commands.Context,
        user: discord.Member = None,
        time: int = 5,
        *,
        reason: str = "Because of naughtiness",
    ):
        if user == self.bot.user:
            await ctx.send("You can't mute me!")
            return
        elif user == ctx.author:
            await ctx.send("You can't mute yourself!")
            return
        role = discord.utils.get(ctx.guild.roles, name="Suppressed")
        if not role:
            try:
                muted = await ctx.guild.create_role(
                    name="Suppressed", reason="To use for muting"
                )
                for channel in ctx.guild.channels:
                    await channel.set_permissions(
                        muted,
                        send_messages=False,
                        read_message_history=False,
                        read_messages=False,
                    )
            except discord.Forbidden:
                return await ctx.send("I have no permissions to make a muted role")
        await user.add_roles(role)
        channel = self.bot.get_channel(Channels.modlog)
        await channel.send(
            f"`{ctx.author.mention}` muted `{user.mention}` for `{time}` minute(s) for reason `{reason}`."
        )
        await asyncio.sleep(time * 60)
        await user.remove_roles(role)

    @commands.command(aliases=["yeetmsg"])
    @commands.has_role("Cat Devs")
    async def purge(
        self, ctx: commands.Context, limit: int, *, reason: str = None
    ) -> None:
        if not 0 < int(limit) < 200:
            await ctx.send("Please purge between 0 and 200 messages.")
            return

        await ctx.channel.purge(limit=limit)
        channel = self.bot.get_channel(Channels.modlog)
        await channel.send(
            f"{ctx.message.author.mention} purged at most `{limit}` messages for reason `{reason}`."
        )


def setup(bot: commands.Bot):
    """Loads cog."""
    bot.add_cog(Moderation(bot))
