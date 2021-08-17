import os
from pathlib import Path

from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv
from loguru import logger
from tortoise import Tortoise

from .utilities import config

load_dotenv(dotenv_path=Path(".env"))
PREFIX = config("bot")["bot"]["prefix"]

DATABASE_URL = os.getenv("DATABASE_URL")


def find_extensions() -> None:
    """Search the exts directory to find cogs to load."""
    for path in Path("bot/exts").rglob("**/*.py"):
        # Convert a path like " botexts/foo/bar.py" to "bot.exts.foo.bar"
        yield path, path_to_module(path)


def path_to_module(path: Path) -> str:
    """Convert a path like "bot/exts/foo/bar.py" to "bot.exts.foo.bar"."""
    return str(path.parent.as_posix()).replace("/", ".") + f".{path.stem}"


async def init_orm():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={
            "models": ["bot.database.models"],
        },
    )

    await Tortoise.generate_schemas()


class CatBot(Bot):
    def __init__(self, *args, **kwargs) -> None:
        config = {
            "command_prefix": commands.when_mentioned_or(PREFIX),
            "case_insensitive": True,
        }

        kwargs.update(config)

        super().__init__(*args, **kwargs)

    async def on_ready(self) -> None:
        """Initialize bot once connected and authorized with Discord."""

        # Start extension loading
        for path, extension in find_extensions():
            logger.info(f"Loading extension {path.stem} " f"from {path.parent}")

            try:
                self.load_extension(extension)
            except Exception as e:  # noqa: E722
                logger.error(
                    f"Failed to load extension {path.stem} " f"from {path.parent}",
                )
                logger.debug(f"Exception:\n{e}")
            else:
                logger.success(f"Loaded extension {path.stem} " f"from {path.parent}")

        # Connect to Postgres
        await init_orm()
