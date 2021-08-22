import os
import typing
from datetime import date, datetime

import discord
from discord.ext.commands import Cog, Context, has_any_role, group
from discord.user import User
from loguru import logger

from bot.bot import CatBot

UserObject = typing.Union[discord.User, discord.Member]
UserSnowflake = typing.Union[UserObject, discord.Object]

class Extensions(Cog):
    
    def __init__(self, bot: CatBot) -> None:
        self.bot = bot
    
    async def mod_log(
        self,
        author: discord.Member,
        cogs_reloaded: list[str]
    ) -> None:

        red = 0xCD6D6D

        color = red #SET COLOUR PREFERENCE

        embed = discord.Embed(
            title=f"Cogs Reloaded:",
            description=f"The Following cogs were reloaded: \n{'\n'.join(cogs_reloaded)}\n",
            timestamp=datetime.utcnow(),
            thumbnail=author.avatar_url,
            color=color,
            footer=f"Requested by: {author.name}"
        )
        channel = self.bot.get_channel(834500035982786620)
        await channel.send(embed=embed)
    
    @group()
    @has_any_role(833841708805652481)
    async def sudo(self, ctx):
        pass

    #
    @sudo.command(name='listdirs', aliases=['ls'])
    async def listdirs(self, ctx, path: str = '..'):

        """Usage: --sudo ls <path: optional = ..>"""

        if os.path.exists(path):

            dirs = os.listdir(path=path)
            await ctx.send(f"```\n{'\n'.join(dirs)}```")

        else:

            embed = discord.Embed(
                title="No can do, m8.",
                description="This path does not exist.",
                timestamp=datetime.utcnow(),
                color=0xCD6D6D
            )
            await ctx.send(embed=embed)
    
    @sudo.command(name='reload')
    async def reload(self, ctx, *args):

        """"Usage: --sudo reload <cogs: optional = all cogs>"""

        await ctx.send("Please wait...")

        if args:
            for argument in args:
                if argument not in self.bot.cogs.keys():
                    await ctx.send(f"{argument} not found.")
                    return
            
            for argument in args:
                self.bot.reload_extension(argument)
            
            await ctx.send('Reloaded all given cogs.')
        else:
            for cog in self.bot.cogs.keys():
                self.bot.reload_extension(cog)
            
            await ctx.send('Reloaded all cogs.')
    
    @sudo.command(name='listcogs', aliases=['lc'])
    async def listcogs(self, ctx):

       """Usage: --sudo listcogs"""

       await ctx.send(f"```\n{'\n'.join(self.bot.cogs.keys())}```")
       
    @sudo.command(name='unload')
    async def unload(self, ctx, *args):

        """"Usage: --sudo unload <cogs: optional = all cogs>"""

        await ctx.send("Please wait...")

        if args:
            for argument in args:
                if argument not in self.bot.cogs.keys():
                    await ctx.send(f"{argument} not found.")
                    return
            
            for argument in args:
                self.bot.unload_extension(argument)
            
            await ctx.send('Unloaded all given cogs.')
        else:
            for cog in self.bot.cogs.keys():
                self.bot.unload_extension(cog)
            
            await ctx.send('Unloaded all cogs.')

def setup(bot: CatBot) -> None:
    """Add cog to bot."""
    bot.add_cog(Extensions(bot))
