from discord.ext import commands
from discord.ext.commands import Context
import discord 





class LeaveServeur(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(LeaveServeur(bot))

        