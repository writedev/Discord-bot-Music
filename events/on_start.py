from discord.ext import commands
import discord
import wavelink

class OnStart(commands.Cog):
  def __init__(self, bot : commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_connect(self):
    url = "http://127.0.0.1:2333"
    nodes = [wavelink.Node(uri=url, password="bye_7")]
    await wavelink.Pool.connect(nodes=nodes, client=self.bot, cache_capacity=100)
    print(f"Connected in lavalink server : {url}")


async def setup(bot):
    await bot.add_cog(OnStart(bot))