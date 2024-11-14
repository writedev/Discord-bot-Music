from discord.ext import commands
from discord.ext.commands import Context
import discord
from typing import cast
import wavelink
from datetime import timedelta


class MusiqueControl(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def join(self, ctx: Context):
        try:
            channel_author = ctx.author.voice.channel.id
            channel_bot = ctx.channel.guild.me.voice.channel.id

            if channel_author == channel_bot:
                return await ctx.send("je suis deja dans ton channel")
            elif channel_author != channel_bot:
                try:
                    point_channel = await self.bot.get_channel(channel_author).connect()
                    return await ctx.send("le bot est connecté au channel")
                except discord.ClientException:
                        await ctx.voice_client.disconnect()
                        return await ctx.voice_client.connect(point_channel)
        except AttributeError:
            await ctx.author.voice.channel.connect()
            await ctx.send("je suis connecté dans ton channel")

    @join.error
    async def join_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("tu dois etre dans un channel")


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
        embed = discord.Embed(title="Music info 🎼",description=f"{music_title} **by** {music_author}",color=0xa6e712 )
        embed.set_thumbnail(url=music_image)
        embed.add_field(name="Titre ✨", value=f"`{music_title}`", inline=False) #music_title, inline=False)
        embed.add_field(name="Auteur ✍️", value=music_author, inline=True)
        embed.add_field(name="Durée 🕰️", value=f"`{duration}`", inline=True)
        embed.add_field(name="Volume 🔊", value=f"`{player.volume}%`", inline=False)
        embed.add_field(name="URL 🔗", value=f"[Cliquez ici]({player.current.uri})", inline=False)
        await ctx.send(embed=embed, ephemeral=True, delete_after=10)
    
    @commands.hybrid_command(name="previous")
    async def previous_playlist(self,ctx : Context):
        player : wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        previous_track = player.queue.history[-1]
        await player.play(previous_track)
        embed = discord.Embed(description=f"The track **{previous_track.title}** by **{previous_track.author}** has been skipped. source : {previous_track.source}", color=0xa6e712)
        await ctx.send(embed=embed, ephemeral=True, delete_after=3)

    @commands.hybrid_command(name="skip", description="Skip a song.")
    async def _skip(self, ctx):
        player: wavelink.Player = ctx.guild.voice_client

        if player and player.queue.is_empty:
            if player.autoplay == wavelink.AutoPlayMode.disabled:
                await ctx.send("```⛔ Autoplay is disabled.```")
            elif player.autoplay == wavelink.AutoPlayMode.enabled:
                await player.skip(force=True)
                await ctx.send("```Skipped the current song.```")
        else:
            await ctx.send("```⛔ Nothing is currently playing.```")

    @commands.hybrid_command(name="volume", aliases=["v"])
    async def change_volume(self, ctx: Context, volume: int):
        player: wavelink.Player = ctx.guild.voice_client
        if volume > 150:
            volume = 150
        elif volume < 0:
            volume = 0
        if player and player.playing == True:
            await player.set_volume(volume)
            await ctx.send(f"```Changed volume to {volume}%```")
        else:
            await ctx.send("```⛔ Nothing is currently playing.```")

    @commands.hybrid_command(name="stop", aliases=["disconnect", "dc"])
    async def stop(self, ctx: Context):
        player: wavelink.Player = ctx.guild.voice_client
        if player and player.playing == True:
            await player.stop()
            await ctx.send("```Stopped the player.```")
        else:
            await ctx.send("```⛔ Nothing is currently playing.```")

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