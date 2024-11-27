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
            embed=discord.Embed(title=f"Volume has been lowered, the volume is **{volume}**",color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)

        low_volume_button.callback = callback_low_volume_button
        
        # high_volume button

        high_volume_button = discord.ui.Button(label="volume",emoji="<:hight_volume:1304587386407227392>", style=discord.ButtonStyle.green)

        async def callback_high_volume_button(interaction : discord.Interaction):
            volume = player.volume + 10
            if volume > 150:
                volume = 150
            elif volume < 0:
                volume = 0
            await player.set_volume(volume)
            embed=discord.Embed(title=f"Volume has been, the volume is **{volume}**",color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)

        high_volume_button.callback = callback_high_volume_button

        # stop button

        stop_button = discord.ui.Button(label="stop",emoji="<:stop_button:1303776558833467392>", style=discord.ButtonStyle.red)

        async def callback_stop_button(interaction : discord.Interaction):
            embed = discord.Embed(title="Stopped", description="The player has been stopped",color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)
            await player.stop()
            await interaction.guild.voice_client.disconnect()
            await self.master_message_play_command.delete()

        stop_button.callback = callback_stop_button

        # skip button

        skip_button = discord.ui.Button(label="skip ",emoji="<:skip_button:1303784286603972679>", style=discord.ButtonStyle.green)

        async def callback_skip_button(interaction : discord.Interaction):
            if player and player.queue.is_empty:
                if player.autoplay == wavelink.AutoPlayMode.disabled:
                    await interaction.response.send_message("```⛔ Autoplay is disabled.```")
                elif player.autoplay == wavelink.AutoPlayMode.enabled:
                    await player.skip(force=True)
                    await interaction.response.send_message("```Skipped the current song.```")
            else:
                await interaction.response.send_message("```⛔ Nothing is currently playing.```")

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
            embed=discord.Embed(title="Autoplay mode has been enabled",color=discord.Color.blue())
            player.autoplay = wavelink.AutoPlayMode.enabled
            dj_button.style = discord.ButtonStyle.red
            dj_button.label = "Disable DJ mode"
            await interaction.message.edit(view=view)
            await interaction.response.send_message(embed=embed,ephemeral=True, delete_after=5)
            dj_button.callback = callback_disable_autoplay_button

        # disable autoplay button

        async def callback_disable_autoplay_button(interaction : discord.Interaction):
            embed=discord.Embed(title="Autoplay mode has been disabled",color=discord.Color.blue())
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
            embed=discord.Embed(title="The player has been paused",color=discord.Color.blue())
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
            embed=discord.Embed(title="The player has been resumed",color=discord.Color.blue())
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

        # Vérifie si l'utilisateur est déjà dans le dictionnaire pour éviter les erreurs
        if ctx.author.id not in self.call_user:
            try:
                player = await ctx.author.voice.channel.connect(cls=wavelink.Player)  # Connecte le bot
                self.call_user[ctx.author.id] = player  # Ajoute l'utilisateur au dictionnaire
            except AttributeError:
                embed = discord.Embed(description=f"{ctx.author.mention} You must be in a voice channel to use this command", color=discord.Color.blue())
                await ctx.send(embed=embed, delete_after=5)
                return
            except discord.ClientException:
                embed = discord.Embed(description=f"{ctx.author.mention} I'm already connected to a voice channel", color=discord.Color.blue())
                await ctx.send(embed=embed, delete_after=3)
                return
        else:
            player = self.call_user[ctx.author.id]  # Récupère l'instance du joueur existant si déjà connecté
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
            milli_duree = str(timedelta(milliseconds=track.length))
            embed = discord.Embed(title="Ajout de la musique dans la piste", description=f"ajout de **``{track}``** par **``{track.author}``** d'une durée de **``{milli_duree}``** min ", color=discord.Color.blue())
            explain_command = f"</explain_play_button:{1304912089558814721}>"
            # Information part
            embed.add_field(name="**Information**",value=f"Pour avoir des explication sur les boutons : \n {explain_command}")
            self.master_message_play_command = await ctx.send(embed=embed, view=view)
            await player.queue.put_wait(track)

        if not player.playing:
            # Play now since we aren't playing anything...
            await player.play(player.queue.get(), volume=20)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if member.id in self.call_user:
            voice_client = self.call_user[member.id]
            if before.channel is not None and after.channel is None:  # Vérifie si l'utilisateur quitte le canal
                await voice_client.disconnect()  # Déconnecte le bot
                del self.call_user[member.id]  # Retire l'utilisateur du dictionnaire


    @commands.hybrid_command(name="join", aliases=["connect"])
    async def join(self, ctx: Context):
        if ctx.author.id in self.call_user:
            embed = discord.Embed(
                description=f"{ctx.author.mention} You are already connected to a voice channel ✅",
                color=discord.Color.blue(),
            )
            await ctx.send(embed=embed, delete_after=3)
            return

        try:
            voice_channel = ctx.author.voice.channel
            voice_client = await voice_channel.connect()  # Connecte le bot au salon vocal
            self.call_user[ctx.author.id] = voice_client  # Associe l'utilisateur au client vocal
            embed = discord.Embed(
                description=f"{ctx.author.mention} I'm connected to the voice channel **{voice_channel.name}** ✅",
                color=discord.Color.blue(),
            )
            await ctx.send(embed=embed, delete_after=3)
        except AttributeError:
            embed = discord.Embed(
                description=f"{ctx.author.mention} You must be in a voice channel to use this command.",
                color=discord.Color.blue(),
            )
            await ctx.send(embed=embed, delete_after=5)
        except discord.ClientException:
            embed = discord.Embed(
                description=f"{ctx.author.mention} I'm already connected to a voice channel.",
                color=discord.Color.blue(),
            )
            await ctx.send(embed=embed, delete_after=3)

async def setup(bot):
    await bot.add_cog(Play(bot))
