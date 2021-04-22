import discord
from discord.ext import commands
import yaml

from bot.utilities.tio import Tio

with open("config.yml", "r") as file:
    colors = yaml.load(file)["colors"]

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["e"])
    async def eval(self, ctx: commands.Context, language: str = "python3", *, code: str = None):
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
                color=colors["green"]
            )
        else:
            embed=discord.Embed(
                title="Eval Results",
                description=f":warning: Your {language} job finished with exit code {exitcode}.",
                color=colors["red"]
            )
        embed.add_field(
            name="Output",
            value=f"```{message}```"
        )
        await ctx.send(embed=embed)
    
def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))