from discord.ext import commands
import discord
import wavelink

class OnStart(commands.Cog):
  def __init__(self, bot : commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def setup_hook(self):
    nodes = [wavelink.Node(uri="http://localhost:2333", password="bye_7")]
    await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=100)


async def setup(bot):
    await bot.add_cog(OnStart(bot))