import os
from pathlib import Path

from dotenv import load_dotenv

from bot.bot import CatBot

load_dotenv(dotenv_path=Path(".env"))


def start() -> None:
    """Entrypoint for Bot."""
    bot = CatBot()
    bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    start()
