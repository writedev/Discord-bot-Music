from discord.ext import commands
import discord
from discord.ext.commands import Context
import wavelink
from typing import cast
from datetime import timedelta
import asyncio






class Play(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.master_message_play_command = None
        self.pause_message = None

    @commands.command()
    async def play(self, ctx: Context, *, query):
        player: wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)

        view = discord.ui.View()

        # stop button

        stop_button = discord.ui.Button(label="stop",emoji="<:stop_button:1303776558833467392>", style=discord.ButtonStyle.red)

        async def callback_stop_button(interaction : discord.Interaction):
            embed = discord.Embed(title="Stopped", description="The player has been stopped",color=0xa6e712)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await player.stop()
            await interaction.guild.voice_client.disconnect()
            await self.master_message_play_command.delete()

        stop_button.callback = callback_stop_button

        # skip button

        skip_button = discord.ui.Button(label="skip ",emoji="<:skip_button:1303784286603972679>", style=discord.ButtonStyle.green)

        async def callback_skip_button(interaction : discord.Interaction):
            await player.skip()
            await interaction.response.send_message("Skipped", ephemeral=True)

        skip_button.callback = callback_skip_button

        # return button

        return_button = discord.ui.Button(label="return",emoji="<:return_button:1303816930402238546>", style=discord.ButtonStyle.green)

        async def callback_return_button(interaction : discord.Interaction):
            await 
            await interaction.response.send_message("Returned", ephemeral=True)

        return_button.callback = callback_return_button

        # autoplay button

        dj_button = discord.ui.Button(label="DJ mode",emoji="<:dj_button:1303814947242770436>", style=discord.ButtonStyle.primary)

        async def callback_autoplay_button(interaction : discord.Interaction):
            embed=discord.Embed(title="Autoplay mode has been enabled",color=0xa6e712)
            player.autoplay = wavelink.AutoPlayMode.enabled
            await interaction.response.send_message(embed=embed,ephemeral=True)

        dj_button.callback = callback_autoplay_button

        # pause button

        pause_button = discord.ui.Button(label="pause",emoji="<:pause_button:1303776999864799313>", style=discord.ButtonStyle.green)  

        async def callback_pause_button(interaction : discord.Interaction):
            await player.pause(True)
            embed=discord.Embed(title="The player has been paused",color=0xa6e712)
            pause_button.emoji = "<:resume_button:1303780254242050189>"
            pause_button.label = "resume"
            await interaction.message.edit(view=view)
            self.pause_message = await interaction.response.send_message(embed=embed, ephemeral=True)
            pause_button.callback = resume_button

        pause_button.callback = callback_pause_button

        async def resume_button(interaction : discord.Interaction):
            await player.pause(False)
            print(self.pause_message)
            pause_button.emoji = "<:pause_button:1303776999864799313>"
            pause_button.label = "pause"
            embed=discord.Embed(title="The player has been resumed",color=0xa6e712)
            await interaction.message.edit(view=view)
            resume_meesage = await interaction.response.send_message(embed=embed, ephemeral=True)

        #cense des bouton
        
        view.add_item(return_button)
        view.add_item(stop_button)
        view.add_item(pause_button)
        view.add_item(skip_button)
        view.add_item(dj_button)

        #   

        if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # type: ignore
            except AttributeError:
                embed = discord.Embed(title=f"{ctx.author.global_name} You must be in a voice channel to use this command", color=0xa6e712)
                message = await ctx.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()
                return
            except discord.ClientException:
                embed = discord.Embed(title=f"{ctx.author.mention} I'm already connected to a voice channel ", color=0xa6e712)
                message = await ctx.send(embed=embed, ephemeral=True)
                await asyncio.sleep(3)
                await message.delete()
                return

        # add dj mode
        player.autoplay = wavelink.AutoPlayMode.enabled

        tracks: wavelink.Search = await wavelink.Playable.search(query)

        if isinstance(tracks, wavelink.Playlist):
            embed = discord.Embed(title="Added to queue", description=f"**``{tracks}``** added to queue by {tracks.author}", color=0xa6e712)
            self.master_message_play_command = await ctx.send(embed=embed, view=view)
        else:
            track: wavelink.Playable = tracks[0]
            milli_duree = timedelta(milliseconds=track.length)
            embed = discord.Embed(title="Added to queue", description=f"**``{track}``** added to queue by {track.author} qui dure {milli_duree} min ", color=0xa6e712)
            self.master_message_play_command = await ctx.send(embed=embed, view=view)
            await player.queue.put_wait(track)
        
        # join channel part
        try:
            channel_author = ctx.author.voice.channel.id
            channel_bot = ctx.channel.guild.me.voice.channel.id

            if channel_author == channel_bot:
                return await player.play(track, volume=20)
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


    @commands.command(aliases=["dc", "dis","stop"])
    async def disconnect(self, ctx: Context):
        player: wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)
        await player.stop()
        await ctx.voice_client.disconnect()



async def setup(bot):
    await bot.add_cog(Play(bot))