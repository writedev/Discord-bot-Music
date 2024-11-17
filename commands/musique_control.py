from discord.ext import commands
from discord.ext.commands import Context
import discord
from typing import cast
import wavelink
from datetime import timedelta


class MusiqueControl(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(aliases=["info_music", "play_info"])
    async def music_info(self, ctx: Context):
        player : wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        # calcul time of music and position
        duration = str(timedelta(milliseconds=player.current.length))
        music_image = player.current.artwork
        # music info
        music_title= f"`{player.current.title}`"
        music_author = f"`{player.current.author}`"
        # ajout dans l'embed
        embed = discord.Embed(color=0xa6e712 )
        embed.set_thumbnail(url=music_image)
        embed.add_field(name="Titre ✨", value=f"`{music_title}`", inline=True) #music_title, inline=False)
        embed.add_field(name="Auteur ✍️", value=music_author, inline=True)
        embed.add_field(name="Durée 🕰️", value=f"`{duration}`", inline=False)
        embed.add_field(name="Volume 🔊", value=f"`{player.volume}%`", inline=True)
        embed.add_field(name="URL 🔗", value=f"[Cliquez ici]({player.current.uri})", inline=False)
        await ctx.send(embed=embed, ephemeral=True, delete_after=15)

    @commands.hybrid_command(name="previous")
    async def previous_playlist(self,ctx : Context):
        player : wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        previous_track = player.queue.history[-1]
        await player.play(previous_track)
        embed = discord.Embed(description=f"The track **{previous_track.title}** by **{previous_track.author}** has been skipped. source : {previous_track.source}", color=0xa6e712)
        await ctx.send(embed=embed, ephemeral=True, delete_after=3)

    @commands.hybrid_command(name="skip", description="Skip a song.")
    async def skip(self, ctx):
        player: wavelink.Player = ctx.guild.voice_client

        if player and player.queue.is_empty:
            if player.autoplay == wavelink.AutoPlayMode.disabled:
                await ctx.send("```⛔ Dj mode is disabled.```")
            elif not player.queue.is_empty:
                await player.skip()
            elif player.autoplay == wavelink.AutoPlayMode.enabled:
                await player.skip(force=True)
                await ctx.send("```Skipped the current song.```")
        else:
            await ctx.send("```❌ Nothing is currently playing.```")

    @commands.hybrid_command(name="volume", aliases=["v"])
    async def change_volume(self, ctx: Context, percentage: int):
        player: wavelink.Player = ctx.guild.voice_client
        if percentage > 150:
            percentage = 150
        elif percentage < 0:
            percentage = 0
        if player and player.playing == True:
            await player.set_volume(percentage)
            embed = discord.Embed(title=f"Volume has been changed to {percentage}% ✅", color=0xa6e712)
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)
        else:
            embed = discord.Embed(description="❌ Nothing is currently playing.",color=0xa6e712)
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)

    @commands.hybrid_command(name="stop")
    async def stop(self, ctx: Context):
        player: wavelink.Player = ctx.guild.voice_client
        if player and player.playing == True:
            await player.stop()
            embed = discord .Embed(description="The player has been stopped ✅",color=0xa6e712)
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)
        else:
            embed = discord .Embed( description="❌ Nothing is currently playing.",color=0xa6e712)
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)

    @commands.hybrid_command(name="disconnect", aliases=["dc","dis"])
    async def disconnect(self, ctx: Context):
        if ctx.voice_client:
            await ctx.voice_client.disconnect(force=True)
            embed = discord.Embed(description="The player has been disconnected ✅",color=0xa6e712)
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)
        else:
            embed = discord.Embed(description="❌ Nothing is currently connected.",color=0xa6e712)
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)


    @commands.hybrid_command(name="explain_active_dj_mode")
    async def explain_active_dj_mode(self, ctx: Context):
        embed = discord.Embed(title="Explain active dj mode", color=0xa6e712)
        embed.set_image(url="https://i.imgur.com/vxKHn2Q.png")
        await ctx.send(embed=embed,)

"""    @commands.hybrid_command(aliases=["next"])
    async def skip(self, ctx: Context):
        player: wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        current_track = player.current
        await player.skip()
        embed = discord.Embed(title="Skipped", description=f"The track **{current_track.title}** by **{current_track.author}** has been skipped. source : {current_track.source}", color=0xa6e712)
        await ctx.send(embed=embed, ephemeral=True)"""

"""    @commands.hybrid_command(name="previous")
    async def previous_playlist(self,ctx : Context):
        player : wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        previous_track = player.queue.history[-1]
        await player.queue.put(previous_track)
        await player.play(previous_track)"""
"""
    @commands.hybrid_command(name="history")
    async def history(self,ctx : Context):
        player : wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            embed = discord.Embed(title="Not connected", description="There music so there are not volume", color=0xa6e712)
            await ctx.send(embed=embed, ephemeral=True)
        else:
            history = player.queue.history  
            embed = discord.Embed(title="History", description=f"The history is : \n {history}", color=0xa6e712)
            await ctx.send(embed=embed, ephemeral=True, delete_after=7)"""

async def setup(bot : commands.Bot):
    await bot.add_cog(MusiqueControl(bot))