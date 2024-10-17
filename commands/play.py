from discord.ext import commands
import discord
from discord.ext.commands import Context
import wavelink
from typing import cast


class Play(commands.Cog):
  def __init__(self, bot : commands.Bot):
    self.bot = bot


  @commands.hybrid_command()  
  async def play(self, ctx : Context, query):
        player : wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client) 
        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # type: ignore
            except AttributeError:
                await ctx.send("Please join a voice channel first before using this command.")
                return
            except discord.ClientException:
                await ctx.send("I was unable to join this voice channel. Please try again.")
                return
        tracks: wavelink.Search = await wavelink.Playable.search(query)
        if isinstance(tracks, wavelink.Playlist):
                print(f"la playist est {tracks}")
                await ctx.send(f"Lancement de la playlist **``{tracks}``**")
        else:
            track : wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            await ctx.send(f"Lancement de la chanson **``{track}``**")

        if not player.playing:
            await player.play(player.queue.get(), volume=8, replace=True)

async def setup(bot):
    await bot.add_cog(Play(bot))