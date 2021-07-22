import os
import pathlib
import traceback

from aiohttp import ClientSession
from discord import Embed, Intents, ActivityType, Activity, HTTPException, utils
from discord.ext import commands
from loguru import logger
from dotenv import load_dotenv

from .utilities import get_yaml_val

load_dotenv(dotenv_path=pathlib.Path(".env"))

PREFIX = get_yaml_val("config.yml", "bot")["bot"]["prefix"]
EXTPATH = get_yaml_val("config.yml", "bot")["bot"]["extpath"]
TOKEN = os.getenv("TOKEN")
BOT_REPO_URL = get_yaml_val("config.yml", "bot")["bot"]["bot_repo_url"]
CHANNELS = get_yaml_val("config.yml", "guild")["guild"]["channels"]
STATUS = get_yaml_val("config.yml", "bot")["bot"]["status"]["text"].replace(
    "{}", PREFIX
)
COLORS = get_yaml_val("config.yml", "colors")["colors"]
ROLES = get_yaml_val("config.yml", "guild")["guild"]["roles"]

EXTPATH = pathlib.Path(EXTPATH)


class Bot(commands.Bot):
    """The core of the bot. Taken from https://github.com/gurkult/gurkbot."""

    def __init__(self) -> None:
        intents = Intents.default()
        intents.members = True
        intents.presences = True

        self.http_session = ClientSession()
        super().__init__(command_prefix=PREFIX, help_command=None, intents=intents)

    def load_extensions(self) -> None:
        """Load all the extensions in the exts/ folder."""
        logger.info("Start loading extensions from ./exts/")
        for extension in EXTPATH.glob("*/*.py"):
            if extension.name.startswith("_"):
                continue  # ignore files starting with _
            dot_path = str(extension).replace(os.sep, ".")[:-3]

            self.load_extension(dot_path)
            logger.info(f"Successfully loaded extension:  {dot_path}.")

    def run(self) -> None:
        """Run the bot with the token in constants.py/.env ."""
        logger.info("Starting bot.")
        if TOKEN is None:
            raise EnvironmentError(
                "token value is None. "
                "Make sure you have configured the TOKEN field in .env"
            )
        super().run(TOKEN)

    async def on_ready(self) -> None:
        """Ran when the bot has connected to discord and is ready."""
        logger.info("Bot online.")
        await self.startup_greeting()
        self.load_extensions()
        activity = Activity(type=ActivityType.listening, name=STATUS)
        await self.change_presence(activity=activity)

    async def startup_greeting(self) -> None:
        """Announce presence to the devlog channel."""
        embed = Embed(description="Connected!")
        embed.set_author(name="Catbot", url=BOT_REPO_URL, icon_url=self.user.avatar_url)
        await self.get_channel(CHANNELS["dev_log"]).send(embed=embed)

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound,)

        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f"{ctx.command} has been disabled.")
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(
                    f"{ctx.command} can not be used in Private Messages."
                )
            except HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if (
                ctx.command.qualified_name == "tag list"
            ):  # Check if the command being invoked is 'tag list'
                await ctx.send("I could not find that member. Please try again.")

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            channel = self.get_channel(CHANNELS["error_log"])
            embed = Embed(
                title=f"Exception in command {ctx.command}:", color=COLORS["red"]
            )
            if len("".join(traceback.format_tb(error.__traceback__))) > 1000:
                newerror = "".join(traceback.format_tb(error.__traceback__))
                newerror = newerror[:1000]
                newerror += "..."
                embed.description = f"```{newerror}```"
                embed.set_footer(text="Truncated... Too long.")
            else:
                embed.description = (
                    f"```{''.join(traceback.format_tb(error.__traceback__))}```"
                )
            await channel.send(embed=embed)

    async def on_member_join(self, member):
        role = utils.get(member.guild.roles, id=ROLES["friends"])

        await member.add_roles(role)

    async def close(self) -> None:
        """Close Http session when bot is shutting down."""
        await super().close()

        if self.http_session:
            await self.http_session.close()
