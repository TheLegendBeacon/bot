import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

PREFIX = os.getenv("PREFIX") or "!"
TOKEN = os.getenv("TOKEN")

EXTENSIONS = pathlib.Path("bot/exts/")
BOT_REPO_URL = "https://github.com/cat-dev-group/bot"

MESSAGE_LIMIT = 2000


class Channels:
    devlog = 809125747037306960
    modlog = 834500035982786620
