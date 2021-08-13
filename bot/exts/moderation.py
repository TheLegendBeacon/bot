import typing
from datetime import datetime

import discord
from discord.ext.commands import Cog, Context, command, has_any_role
from loguru import logger

from bot.bot import CatBot

# Type aliases
UserObject = typing.Union[discord.User, discord.Member]
UserSnowflake = typing.Union[UserObject, discord.Object]


class Moderation(Cog):
    """Apply and pardon infractions on users for moderation purposes."""

    def __init__(self, bot: CatBot):
        self.bot = bot

    async def mod_log(
        self,
        infraction: str,
        member: UserSnowflake,
        actor: UserSnowflake,
        positive: bool = None,
        reason: str = None,
    ) -> None:

        blurple = 0x7289DA
        green = 0x68C290
        red = 0xCD6D6D

        if positive:
            color = green
        elif not positive:
            color = red
        else:
            color = blurple

        embed = discord.Embed(
            title=f"Infraction applied: {infraction}",
            description=f"**Member:** <@{member.id}> (`{member.id}`)\n\
                **Actor:** <@{actor.id}> (`{actor.id}`)\n\
                **Reason:** {reason}",
            timestamp=datetime.utcnow(),
            color=color,
        )
        channel = self.bot.get_channel(834500035982786620)
        await channel.send(embed=embed)

    @command()
    @has_any_role(833841708805652481)
    async def ban(
        self,
        ctx: Context,
        user: UserSnowflake,
        reason: typing.Optional[str],
    ) -> None:
        try:
            await ctx.guild.ban(user=user, reason=reason, delete_message_days=0)
        except Exception as e:
            await ctx.send(f"Failed to ban {user} from the server.")
            logger.error(f"Failed to ban {user} from the server.")
            logger.debug(f"Exception:\n{e}")
        else:
            await ctx.send(f"Banned {user} from the server.")
            await self.mod_log(
                infraction="ban",
                member=user,
                actor=ctx.author,
                reason=reason,
                positive=False,
            )
            logger.success(f"Banned {user} from the server.")

    @command()
    @has_any_role(833841708805652481)
    async def unban(
        self,
        ctx: Context,
        user: UserSnowflake,
        reason: typing.Optional[str],
    ) -> None:
        try:
            await ctx.guild.unban(user=user, reason=reason)
        except Exception as e:
            await ctx.send(f"Failed to unban {user} from the server.")
            logger.error(f"Failed to unban {user} from the server.")
            logger.debug(f"Exception:\n{e}")
        else:
            await ctx.send(f"Unbanned {user} from the server.")
            await self.mod_log(
                infraction="unban",
                member=user,
                actor=ctx.author,
                reason=reason,
                positive=True,
            )
            logger.success(f"Unbanned {user} from the server.")


def setup(bot: CatBot) -> None:
    """Add cog to bot."""
    bot.add_cog(Moderation(bot))
