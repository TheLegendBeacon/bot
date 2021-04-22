import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

PREFIX = os.getenv("PREFIX") or "!"
TOKEN = os.getenv("TOKEN")

EXTENSIONS = pathlib.Path("bot/exts/")
BOT_REPO_URL = "https://github.com/cat-dev-group/bot"

MESSAGE_LIMIT = 2000

NECATIVE_REPLIES = [
    "Nah mate, this ain't gonna work.",
    "**MEOW** nope **MEOW**",
    "Unpoggers.",
    "DA DIVINE CAT says you can't.",
    "Not in a million cat years.",
    "Yeah, no.",
    "<command cannot be executed>",
    "Error code: 3120"
]

DURATION_DICT = {
    "s": 1
    "m": 60
    "h": 3600
    "d": 86400
    "w": 604800
    "M": 2592000
    "y": 31536000
    "D": 315360000
}


class Channels:
    devlog = 809125747037306960
    modlog = 834500035982786620
