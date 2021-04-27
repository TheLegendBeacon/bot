import random

from discord import Embed
from discord.ext import commands

from typing import Optional

from bot.constants import NECATIVE_REPLIES
from bot.utilities import get_yaml_val

COLORS = get_yaml_val("config.yml", "colors")["colors"]

ZEN = [
    "Elegant cattiness is better than ugly.",
    "Explicat is better than implicat.",
    "SimpleCat is better than catplex.",
    "Catplex is better than catplicated.",
    "Fat:cat2: is better than nested:cat2:.",
    "ᓚᘏᗢ is better than sadcat.",
    "Catification counts.",
    "Special cats aren't special enough to be better than ᓚᘏᗢ.",
    "Although practicatity beats purity.",
    "Cats should never pass silently.",
    "Not even when explicatly silenced.",
    "In the face of ᓚᘏᗢ, refuse the tempcation to guess.",
    "There should be one-- and always only one --supreme ᓚᘏᗢ.",
    "Although that may not be obvious at first unless you're ᓚᘏᗢ itself.",
    "NowCat:tm: is better than NeverCat:tm:.",
    "Although NeverCat:tm: is often better than **Right**NowCat:tm:.",
    "If the implemencation is hard to catplain, it's a bad idea.",
    "If the implemencation is easy to catplain, it may be a good idea.",
    "ᓚᘏᗢs are one meowing great idea -- let's do more of those!",
]


class Zen(commands.Cog):
    """Cog for the zencat command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["zenofpycat", "zen"])
    async def zencat(self, ctx: commands.Context, index: Optional[int]) -> None:
        """Sends a modified version of the python zen."""
        rand_color = COLORS[random.choice(list(COLORS.keys()))]

        if index is None:
            zen_embed = Embed(
                title="The Zen of PyCat",
                description="\n".join(ZEN),
                color=rand_color,
            )

            zen_embed.set_footer(
                text="ALL HAIL THE DIVINE ᓚᘏᗢ!", icon_url=self.bot.user.avatar_url
            )

            await ctx.send(embed=zen_embed)
        else:
            try:
                line_embed = Embed(
                    title=(
                        "The Zen of PyCat, line "
                        f"{19 - index * -1 if index < 0 else index}"
                    ),
                    description=ZEN[index],
                    color=rand_color,
                )

                await ctx.send(embed=line_embed)
            except IndexError:
                error_embed = Embed(
                    title=random.choice(NECATIVE_REPLIES),
                    description=(
                        "Ouch! You sent an invalid line index that made my cat "
                        "brain confused. Please enter an integer between -19 and 18!"
                    ),
                    color=COLORS["red"],
                )

                await ctx.send(embed=error_embed)


def setup(bot: commands.Bot) -> None:
    """Loads the Zen cog."""
    bot.add_cog(Zen(bot))
