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
        await player.stop()
        await ctx.voice_client.disconnect()


    @commands.hybrid_command(aliases=["vol", "v"])
    async def volume(self, ctx: Context, volume: int):
        player: wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        self.music_volume = volume
        await player.set_volume(self.music_volume)
        embed=discord.Embed(title=f"Volume has been, the volume is **{self.music_volume}**",color=0xa6e712)
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(aliases=["next"])
    async def skip(self, ctx: Context):
        player: wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        current_track = player.current
        await player.skip()
        embed = discord.Embed(title="Skipped", description=f"The track **{current_track.title}** by **{current_track.author}** has been skipped. source : {current_track.source}", color=0xa6e712)
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="volume_info")
    async def volume_info(self, ctx: Context):
        player : wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        if not player:
            embed = discord.Embed(title="Not connected", description="There music so there are not volume", color=0xa6e712)
            await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Volume Info", description=f"The volume is **{self.music_volume}** `/play`", color=0xa6e712)
            message = await ctx.send(embed=embed)
            await message.delete(delay=5)

async def setup(bot : commands.Bot):
    await bot.add_cog(MusiqueControl(bot))