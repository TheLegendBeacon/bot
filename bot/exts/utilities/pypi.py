import itertools
import random

import discord
from discord.ext import commands
from discord.utils import escape_markdown

from bot.utilities import get_yaml_val

Colors = get_yaml_val("config.yml", "colors")["colors"]

URL = "https://pypi.org/pypi/{package}/json"
PYPI_ICON = "https://cdn.discordapp.com/emojis/766274397257334814.png"

NECATIVE = get_yaml_val("config.yml", "necative")["necative"]

pycolors = itertools.cycle((Colors["yellow"], Colors["blue"]))


class PyPi(commands.Cog):
    """Cog for the PyPi command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def pypi(self, ctx: commands.Context, package: str):
        """Fetches package info from PyPi."""
        embed = discord.Embed(title=random.choice(NECATIVE), colour=Colors["red"])
        embed.set_thumbnail(url=PYPI_ICON)

        async with ctx.typing():
            async with self.bot.http_session.get(
                URL.format(package=package)
            ) as response:

                if response.status == 404:
                    embed.description = "Package not found!"
                elif (
                    response.status == 200
                    and response.content_type == "application/json"
                ):
                    resp_json = await response.json()
                    info = resp_json["info"]

                    embed.title = f'{info["name"]} v{info["version"]}'

                    embed.url = info["package_url"]
                    embed.color = next(pycolors)

                    summary = escape_markdown(info["summary"])

                    if summary and not summary.isspace():
                        embed.description = summary
                    else:
                        embed.description = "Package does not have a summary."

                else:
                    embed.description = (
                        "There was an unforseen error fetching your package."
                    )
                await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    """Loads the PyPi cog."""
    bot.add_cog(PyPi(bot))
