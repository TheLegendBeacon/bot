from typing import Optional

from discord.ext import commands
import discord

from bot.utilities import get_yaml_val
import bot.constants

colors = get_yaml_val("config.yml", "colors")["colors"]


class Help(commands.Cog):
    """Cog for the help command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context, command: Optional[str] = None):
        """This help command."""
        if not command:
            embed = discord.Embed(
                title="Help: All",
                description=f"A detailed list of all commands. For help on a specific command, "
                f"do `{bot.constants.PREFIX}help [command]`.",
                color=colors["light_blue"],
            )

            for element in self.bot.commands:
                commandraw = self.bot.get_command(element.qualified_name)
                help = commandraw.help
                embed.add_field(name=element.qualified_name, value=f"*{help}*")

            await ctx.send(embed=embed)

        elif command not in self.bot.commands:
            commandraw = self.bot.get_command(command.lower())
            if commandraw is None:
                await ctx.send(f"`{command}` is an invalid command!")
                return
            name = commandraw.qualified_name
            help = commandraw.help
            alias_list = commandraw.aliases
            usage = commandraw.signature

            embed = discord.Embed(
                title=f"Help: {name}",
                description=f"*{help}*",
                color=colors["light_blue"],
            )

            aliases = ", ".join(alias_list)
            embed.add_field(
                name="Usage", value=f"`{bot.constants.PREFIX}{name}{usage}`"
            )

            embed.add_field(name="Can also use", value=f"*{aliases}*")
            await ctx.send(embed=embed)
        else:
            command = command.lower()
            commandraw = self.bot.get_command(command)
            command_data = commandraw.help
            alias_list = commandraw.aliases
            command_args = commandraw.signature

            embed = discord.Embed(
                title=f"Help: {command}",
                description=f"*{command_data}*",
                color=colors["light_blue"],
            )

            aliases = ", ".join(alias_list)

            embed.add_field(
                name="Usage", value=f"`{bot.constants.PREFIX}{command}{command_args}`"
            )

            if aliases != "":
                embed.add_field(name="Can also use", value=f"*{aliases}*")

            await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    """Loads cog."""
    bot.add_cog(Help(bot))
