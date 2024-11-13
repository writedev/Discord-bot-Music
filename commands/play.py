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
        self.call_user = {}


    @commands.hybrid_command()
    async def play(self, ctx: Context, *, query):
        player: wavelink.Player
        player = cast(wavelink.Player, ctx.voice_client)

        view = discord.ui.View()

        # low_volume button

        low_volume_button = discord.ui.Button(label="volume",emoji="<:low_volume:1304587618947956749>", style=discord.ButtonStyle.green)

        async def callback_low_volume_button(interaction : discord.Interaction):
            volume = player.volume - 10
            await player.set_volume(volume)
            embed=discord.Embed(title=f"Volume has been lowered, the volume is **{volume}**",color=0xa6e712)
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)

        low_volume_button.callback = callback_low_volume_button
        
        # high_volume button

        high_volume_button = discord.ui.Button(label="volume",emoji="<:hight_volume:1304587386407227392>", style=discord.ButtonStyle.green)

        async def callback_high_volume_button(interaction : discord.Interaction):
            volume = player.volume + 10
            await player.set_volume(volume)
            embed=discord.Embed(title=f"Volume has been, the volume is **{volume}**",color=0xa6e712)
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)

        high_volume_button.callback = callback_high_volume_button

        # stop button

        stop_button = discord.ui.Button(label="stop",emoji="<:stop_button:1303776558833467392>", style=discord.ButtonStyle.red)

        async def callback_stop_button(interaction : discord.Interaction):
            embed = discord.Embed(title="Stopped", description="The player has been stopped",color=0xa6e712)
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)
            await player.stop()
            await interaction.guild.voice_client.disconnect()
            await self.master_message_play_command.delete()

        stop_button.callback = callback_stop_button

        # skip button

        skip_button = discord.ui.Button(label="skip ",emoji="<:skip_button:1303784286603972679>", style=discord.ButtonStyle.green)

        async def callback_skip_button(interaction : discord.Interaction):
            try:
                if not player.queue:
                    await interaction.response.send_message("Il n'y a pas de musique après celle-ci", ephemeral=True, delete_after=5)
                else:
                    await player.skip()
                    await interaction.response.send_message("Skipped", ephemeral=True, delete_after=5)
            except Exception as e:
                await interaction.response.send_message("Il n'y a pas de musique à passer", ephemeral=True, delete_after=5)

        skip_button.callback = callback_skip_button

        # return button

        return_button = discord.ui.Button(label="return",emoji="<:return_button:1303816930402238546>", style=discord.ButtonStyle.green)

        async def callback_return_button(interaction : discord.Interaction):
            previous_track = player.queue.history[-1]
            print(f"previous track : {previous_track}")
            await player.play(previous_track)
            await interaction.response.send_message(f"Returned and {track.title}", ephemeral=True, delete_after=5)

        return_button.callback = callback_return_button

        # autoplay button

        dj_button = discord.ui.Button(label="DJ mode",emoji="<:dj_button:1303814947242770436>", style=discord.ButtonStyle.primary)

        async def callback_enable_autoplay_button(interaction : discord.Interaction):
            embed=discord.Embed(title="Autoplay mode has been enabled",color=0xa6e712)
            player.autoplay = wavelink.AutoPlayMode.enabled
            dj_button.style = discord.ButtonStyle.red
            dj_button.label = "Disable DJ mode"
            await interaction.message.edit(view=view)
            await interaction.response.send_message(embed=embed,ephemeral=True, delete_after=5)
            dj_button.callback = callback_disable_autoplay_button

        # disable autoplay button

        async def callback_disable_autoplay_button(interaction : discord.Interaction):
            embed=discord.Embed(title="Autoplay mode has been disabled",color=0xa6e712)
            player.autoplay = wavelink.AutoPlayMode.disabled
            dj_button.style = discord.ButtonStyle.primary
            dj_button.callback = callback_enable_autoplay_button
            dj_button.label = "DJ mode"
            await interaction.message.edit(view=view)
            await interaction.response.send_message(embed=embed,ephemeral=True, delete_after=5)

        dj_button.callback = callback_enable_autoplay_button
        
        # pause button

        pause_button = discord.ui.Button(label="pause",emoji="<:pause_button:1303776999864799313>", style=discord.ButtonStyle.green)  

        async def callback_pause_button(interaction : discord.Interaction):
            await player.pause(True)
            embed=discord.Embed(title="The player has been paused",color=0xa6e712)
            pause_button.emoji = "<:resume_button:1303780254242050189>"
            pause_button.label = "resume"
            pause_button.style = discord.ButtonStyle.primary
            await interaction.message.edit(view=view)
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)
            pause_button.callback = resume_button

        pause_button.callback = callback_pause_button

        # resume button

        async def resume_button(interaction : discord.Interaction):
            await player.pause(False)
            pause_button.emoji = "<:pause_button:1303776999864799313>"
            pause_button.label = "pause"
            pause_button.style = discord.ButtonStyle.green
            embed=discord.Embed(title="The player has been resumed",color=0xa6e712)
            await interaction.message.edit(view=view)
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)

        #Sens des bouton
        
        view.add_item(return_button)
        view.add_item(stop_button)
        view.add_item(pause_button)
        view.add_item(skip_button)
        view.add_item(dj_button)
        view.add_item(low_volume_button)
        view.add_item(high_volume_button)

        if not player:
            try:
                self.call_user[ctx.author.id]
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # type: ignore
                voice_client = player
                self.call_user[ctx.author.id] = voice_client
            except AttributeError:
                embed = discord.Embed(title=f"{ctx.author.global_name} You must be in a voice channel to use this command", color=0xa6e712)
                await ctx.send(embed=embed, delete_after=5)
                return
            except discord.ClientException:
                embed = discord.Embed(title=f"{ctx.author.mention} I'm already connected to a voice channel ", color=0xa6e712)
                return await ctx.send(embed=embed, ephemeral=True, delete_after=3)
        # Add track to player

        tracks: wavelink.Search = await wavelink.Playable.search(query)

        # add dj mode
        player.autoplay = wavelink.AutoPlayMode.disabled

        if isinstance(tracks, wavelink.Playlist):
            added: int = await player.queue.put_wait(tracks)
            embed = discord.Embed(f"Added the playlist **`{tracks.name}`** ({added} songs) to the queue.")
            
            self.master_message_play_command = await ctx.send(embed=embed, view=view)
        else:
            track: wavelink.Playable = tracks[0]
            milli_duree = timedelta(milliseconds=track.length)
            embed = discord.Embed(title="Ajout de la musique quand la piste", description=f"ajout de **``{track}``** par {track.author} d'une durée de **``{milli_duree}``** min ", color=0xa6e712)
            explain_command = f"</explain_play_button:{1304912089558814721}>"
            # Information part
            embed.add_field(name="**Information**",value=f"Pour avoir des explication sur les boutons : \n {explain_command}")
            self.master_message_play_command = await ctx.send(embed=embed, view=view)
            await player.queue.put_wait(track)

        if not player.playing:
            # Play now since we aren't playing anything...
            self.music_volume = 20
            await player.play(player.queue.get(), volume=20)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id in self.call_user:
            voice_client = self.call_user[member.id]
            if before.channel is not None and after.channel is None:  # Vérifie si l'utilisateur quitte le canal
                await voice_client.disconnect()  # Déconnecte le bot
                del self.call_user[member.id]  # Retire l'utilisateur du dictionnaire
                print(f"Le bot s'est déconnecté car {member.display_name} a quitté le canal vocal.")




        # join channel part
        """try:
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
                        return await ctx.voice_client.connect(point_channel) """
"""     
        # ancienne version      if not player:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # type: ignore
            except AttributeError:
                embed = discord.Embed(title=f"{ctx.author.global_name} You must be in a voice channel to use this command", color=0xa6e712)
                await ctx.send(embed=embed, delete_after=5)
                return
            except discord.ClientException:
                embed = discord.Embed(title=f"{ctx.author.mention} I'm already connected to a voice channel ", color=0xa6e712)
                return await ctx.send(embed=embed, ephemeral=True, delete_after=3)
"""

async def setup(bot):
    await bot.add_cog(Play(bot))
