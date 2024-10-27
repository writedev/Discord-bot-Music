from discord.ext import commands
import discord
from discord.ext.commands import Context
import wavelink
from typing import cast
from datetime import timedelta


class Play(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx: Context, *, query):
        player: wavelink.Player
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
            await ctx.send(f"Lancement de la playlist **``{tracks}``**")
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            milli_duree = timedelta(milliseconds=track.length)
            await ctx.send(f"Lancement de la chanson **``{track}``** faite par {track.author} qui dure {milli_duree} min")
        
        # join channel part
        try:
            channel_author = ctx.author.voice.channel.id
            channel_bot = ctx.channel.guild.me.voice.channel.id

            if channel_author == channel_bot:
                await player.play(track, volume=20)
                return await ctx.send("je suis deja dans ton channel")
            elif channel_author != channel_bot:
                try:
                    point_channel = await self.bot.get_channel(channel_author).connect()
                    await player.play(track, volume=20)
                    return await ctx.send("le bot est connecté au channel")
                except discord.ClientException:
                        await ctx.voice_client.disconnect()
                        return await ctx.voice_client.connect(point_channel)
        except AttributeError:
            await ctx.author.voice.channel.connect()
            await player.play(track, volume=20)
            return await ctx.send("je suis connecté dans ton channel")



    @commands.command()
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




    @commands.command()
    async def stop(self,ctx : Context):
        player: wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        await player.stop()
        await ctx.voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Play(bot))