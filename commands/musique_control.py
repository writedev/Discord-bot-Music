from discord.ext import commands
from discord.ext.commands import Context
import discord
from typing import cast
import wavelink


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


    @commands.hybrid_command(aliases=["dc", "dis","stop"])
    async def disconnect(self, ctx: Context):
        player: wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        await ctx.voice_client.disconnect()
        await player.stop()
        embed = discord.Embed(description="The player has been stopped",color=0xa6e712 )
        await ctx.send(embed=embed, ephemeral=True, delete_after=5)


    @commands.hybrid_command(aliases=["info_music", "play_info"])
    async def music_info(self, ctx: Context):
        player : wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        music_image = player.current.artwork
        music_title= player.current.title
        music_author = player.current.author
        embed = discord.Embed(title="Music info",description=f"{music_title} by {music_author}",color=0xa6e712 )
        embed.set_thumbnail(url=music_image)
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
        if player and player.playing == True:
            await player.stop(force=True)
            await ctx.send("```Skipped the current song.```")
        else:
            await ctx.send("```⛔ Nothing is currently playing.```")

    @commands.hybrid_command(name="volume", aliases=["v"])
    async def change_volume(self, ctx: Context, volume: int):
        player: wavelink.Player = ctx.guild.voice_client
        if volume > 150:
            await ctx.send("```⛔ Volume must be between 0 and 150.```")
        elif player and player.playing == True:
            await player.set_volume(volume)
            await ctx.send(f"```Changed volume to {volume}%```")
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