import discord
from discord.ext import commands
import asyncio
import datetime
from bot.utilities import get_yaml_val


class makeembed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def makeembed(self, ctx):
        """Makes an embed based on parameters set by the user."""
        data = get_yaml_val("config.yml", "colors")["colors"]

        questions = [
            "What is the value of **title**?",
            "What is the value of **description**?",
            "What is the value of **footer**?",
            "What is the value of **author**?",
        ]

        answers = []

        keys = list(data.keys())

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author

        for index, question in enumerate(questions):
            await ctx.send(f"Question {index+1}: {question}")
            msg = await self.bot.wait_for("message", check=check)

            if msg.content == "cancel":
                await ctx.send("Ending Process!")
                return

            answers.append(msg.content)
            await msg.add_reaction("✔️")
            await asyncio.sleep(1)

        while True:
            await ctx.send("What color would you like your embed to be?")
            msg = await self.bot.wait_for("message", check=check)
            content = msg.content

            if content.lower() == "cancel":
                await ctx.send("Ending Process")
                return

            if content.lower() in keys:
                color = data[content.lower()]
                await msg.add_reaction("✔️")
                break

            await msg.add_reaction("❌")
            await ctx.send("Not a valid color!")
            await asyncio.sleep(1)

        embed = discord.Embed(title=answers[0], description=answers[1], color=color)
        embed.set_footer(text=answers[2])
        embed.set_author(name=answers[3], icon_url=ctx.author.avatar_url)
        """ the embed we can make so far """

        fields = 0
        while True:
            if fields < 6:
                await ctx.send(
                    f"Would you like to add an field? ({6 - fields} fields left) Answer Y or N"
                )

                msg = await self.bot.wait_for("message", check=check)

                if (msg.content).lower() == "y":
                    questions = [
                        "What is the value of **name**?",
                        "What is the value of **value**?",
                    ]

                    answers = []

                    for question in questions:
                        await ctx.send(question)
                        msg = await self.bot.wait_for("message", check=check)

                        if msg.content == "cancel":
                            await ctx.send("Ending Process!")
                            fields = 6
                            return

                        else:
                            answers.append(msg.content)
                            await msg.add_reaction("✔️")
                            await asyncio.sleep(1)

                    embed.add_field(name=answers[0], value=answers[1], inline=False)
                    fields += 1

                elif (msg.content).lower() == "n":
                    await ctx.send("Closing!")
                    await asyncio.sleep(1)
                    break

                else:
                    await ctx.send("Please answer with `y` or `n`")

            else:
                await ctx.send("You have no available fields left")
                await asyncio.sleep(1)
                break

        await ctx.send(
            "Would you like an timestamp? Say `yes` or reply with something else for no"
        )
        msg = await self.bot.wait_for("message", check=check)
        if msg.content == "yes":
            embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=embed)

        perms = (ctx.author).guild_permissions

        if perms.administrator == True:

            await ctx.send(
                "Would you like to send the embed somewhere else? (say `yes` or reply something else to not do it)"
            )
            msg = await self.bot.wait_for("message", check=check)

            if (msg.content).lower() == "yes":
                await ctx.send("Tag the channel.")
                msg = await self.bot.wait_for("message", check=check)

                if msg.channel_mentions:

                    text = msg.channel_mentions[0]
                    new = await text.send(embed=embed)

                    em = discord.Embed(description=f"[Sent!]({new.jump_url})")
                    em.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    em.timestamp = datetime.datetime.utcnow()
                    await ctx.send(embed=em)

            else:
                await ctx.send("ok bye")

    @makeembed.error
    async def makeembed_error(self, ctx, error):
        await ctx.send("An Error occured")
        error_report = discord.Embed(
            description=f"```{error}```",
            color=0xFF0000,
            timestamp=datetime.datetime.utcnow(),
        )
        await ctx.send(embed=error_report)


def setup(bot):
    bot.add_cog(makeembed(bot))
