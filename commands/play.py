from discord.ext import commands
import discord
from discord.ext.commands import Context


class Play(commands.Cog):
  def __init__(self, bot : commands.Bot):
    self.bot = bot

  @commands.command()
  async def play(self, ctx: Context, url: str):
    await ctx.send("https://www.youtube.com/watch?v=" + url)



async def setup(bot):
    await bot.add_cog(Play(bot))