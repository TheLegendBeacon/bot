from discord.ext import commands
import discord
import json
import random
import asyncio
from bot.utilities import get_yaml_val
import re
quotechannel = get_yaml_val("bot/config.yml", 'guild')['guild']["channels"]["quotes"]


class Quote(commands.Cog):
    """Cog for the quote command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("quote", aliases=["q"])
    @commands.has_any_role(833841708805652481, 852267769985761281, 839844083463749664)
    async def quote(self, ctx: commands.Context, user: discord.User, *, quote: str):
        """Quotes a user on a sent message."""
        channel = self.bot.get_channel(quotechannel)
        await channel.send(f"{user.mention}: {quote}")
        await ctx.send("Successfully quoted message.")

    @commands.command("activate")
    @commands.has_any_role(833841708805652481, 852267769985761281, 839844083463749664)
    async def activate(self, ctx: commands.Context, id: discord.TextChannel):
        "Used to dynamically change the specified channel name on a regular basis by randomly selecting a quote from quotes.json"
        while True:
            with open(r'bot/resources/quotes.json') as f:
                fil = json.load(f)
            sen = random.choice(fil['quotes'])
            by = fil['authors'][fil['quotes'].index(sen)]
            await id.edit(name=f'ᗢ-ot-{sen[:100]}', topic=f'-By {by} Off-topic discussion.')
            await asyncio.sleep(86400)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 809158704644751370:
            with open(r'bot/bot/resources/quotes.json') as f:
                fil = json.load(f)
            res = ''
            for i in re.compile(r'[^<@!\d+>]').finditer(message.content):
                res += i.group(0)
            name = self.bot.get_user(message.author.id).name
            fil['quotes'].append(res)
            fil['authors'].append(name)
            with open(r'catcord.json', 'w+') as f:
                json.dump(fil, f)


def setup(bot: commands.Bot):
    """Loads the quote cog."""
    bot.add_cog(Quote(bot))
