import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

PREFIX = os.getenv("PREFIX") or "!"
TOKEN = os.getenv("TOKEN")

EXTENSIONS = pathlib.Path("bot/exts/")
BOT_REPO_URL = "https://github.com/cat-dev-group/bot"


class Channels:
    devlog = 809125747037306960
