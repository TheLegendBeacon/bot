import random

import discord
from discord.ext import commands

from typing import Optional

from bot.constants import NECATIVE_REPLIES
from bot.utilities import get_yaml_val

from collections import OrderedDict

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

LEFT_ARROW = "\u2b05\ufe0f"
RIGHT_ARROW = "\u27a1\ufe0f"


class DequeButDict(OrderedDict):
    def __init__(self, maxlen, dct):
        self._max = maxlen
        super().__init__(dct)

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        if len(self) > self._max:
            self.popitem(False)


class Zen(commands.Cog):
    """Cog for the zencat command."""

    msgs_to_check = DequeButDict(5, {})

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def make_line_embed(index, color):
        return discord.Embed(
            title=(
                "The Zen of PyCat, line "
                f"{19 - index * -1 if index < 0 else index}"
            ),
            description=ZEN[index],
            color=color,
        )

    @commands.command(aliases=["zenofpycat", "zen"])
    async def zencat(self, ctx: commands.Context, index: Optional[int]) -> None:
        """Sends a modified version of the python zen."""

        rand_color = COLORS[
            random.choice(
                list(COLORS.keys())
            )
        ]

        if index is None:
            zen_embed = discord.Embed(
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
                line_embed = Zen.make_line_embed(index, rand_color)

                msg = await ctx.send(embed=line_embed)
                Zen.msgs_to_check.update({msg.id: index})

                await msg.add_reaction(LEFT_ARROW)
                await msg.add_reaction(RIGHT_ARROW)
            except IndexError:
                error_embed = discord.Embed(
                    title=random.choice(NECATIVE_REPLIES),
                    description=(
                        "Ouch! You sent an invalid line index that made my cat "
                        "brain confused. Please enter an integer between -19 and 18!"
                    ),
                    color=COLORS["red"],
                )

                await ctx.send(embed=error_embed)

    @commands.Cog.listener("on_reaction_add")
    async def on_reaction_add(
        self, reaction: discord.Reaction, user: discord.User
    ) -> None:
        if user.id == self.bot.user.id:
            return

        re_msg = reaction.message

        for msg_id, line_index in Zen.msgs_to_check.items():
            if re_msg.id == msg_id:
                original_color = re_msg.embeds[0].color

                if reaction.emoji == LEFT_ARROW and line_index > 0:
                    new_index = line_index - 1

                elif reaction.emoji == RIGHT_ARROW and line_index < 18:
                    new_index = line_index + 1

                else:
                    new_index = 0

                line_embed = Zen.make_line_embed(
                    new_index,
                    original_color,
                )

                Zen.msgs_to_check[msg_id] = new_index

                await re_msg.edit(embed=line_embed)
                await re_msg.remove_reaction(reaction, user)


def setup(bot: commands.Bot) -> None:
    """Loads the Zen cog."""
    bot.add_cog(Zen(bot))
