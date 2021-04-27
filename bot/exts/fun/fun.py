import datetime

import discord
from discord.ext import commands
import pytz
import yaml

from bot.utilities.tio import Tio

cst = pytz.timezone("US/Central")

with open("config.yml", "r", encoding="utf-8") as file:
    colors = yaml.load(file)["colors"]


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["e"])
    async def eval(
        self, ctx: commands.Context, language: str = "python3", *, code: str = None
    ):
        """Evaluates code using tio.run."""
        site = Tio()
        if code.strip("`"):
            # Code in message
            code = code.strip("`")
            first_line = code.splitlines()[0]
            if not language.startswith("```"):
                code = code[len(first_line) + 1 :]
        request = site.new_request(language, code)
        raw = site.send(request)
        exitcode = int(raw[-1])
        message = raw[:-14]
        if exitcode == 0:
            embed = discord.Embed(
                title="Eval Results",
                description=f":white_check_mark:  Your {language} job has completed with exit code {exitcode}.",
                color=colors["green"],
            )
        else:
            embed = discord.Embed(
                title="Eval Results",
                description=f":warning: Your {language} job finished with exit code {exitcode}.",
                color=colors["red"],
            )
        embed.add_field(name="Output", value=f"```{message}```")
        await ctx.send(embed=embed)

    @commands.command(aliases=["quack"])
    async def duck(self, ctx, typeofduck: str = "duck") -> None:
        """Generates a random duck or manduck using Quackstack."""
        now = datetime.datetime.now(cst)
        if typeofduck not in ["duck", "manduck"]:
            await ctx.send("That is not a valid duck type!")
            return
        async with ctx.typing():
            async with self.bot.http_session.get(
                f"https://quackstack.pythondiscord.com/{typeofduck}"
            ) as r:
                jsondata = await r.json()
                file = jsondata.get("file")
            embed = discord.Embed(
                title="Ducky Time!",
                description="A duck or manduck from [Quackstack](https://quackstack.pydis.org/docs).",
                color=colors["green"],
            )
            embed.set_image(url=f"https://quackstack.pythondiscord.com{file}")
            embed.set_footer(text=now.strftime("%I:%M %p CST on %d/%m/%Y"))
            await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
