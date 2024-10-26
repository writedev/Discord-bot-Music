from discord.ext import commands
import discord
from discord.ext.commands import Context
import wavelink
from typing import cast


class Play(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
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
            await ctx.send(f"Lancement de la chanson **``{track}``**")

        if not player.playing and ctx.guild.me.voice == ctx.guild.me.voice.channel:
            await player.play(player.queue.get(), volume=12, replace=True)
        elif ctx.guild.me.voice != ctx.guild.me.voice.channel:
            await ctx.author.voice.channel.connect

        # Ajout d'un bouton pour arrêter la musique
        stop_button = discord.ui.Button(label="Arrêter la musique", style=discord.ButtonStyle.danger)

        # Correction : définition correcte du callback asynchrone pour le bouton
        async def stop_callback(interaction: discord.Interaction):
            if player.paused == False:
                await player.pause(not player.paused)
                await interaction.response.send_message("La musique a été arrêtée.", ephemeral=True)
            else:
                await player.pause(not player.paused)
                await interaction.response.send_message("Aucune musique n'est en cours de lecture.", ephemeral=True)

        stop_button.callback = stop_callback  # Assigne la fonction callback directement

        view = discord.ui.View()
        view.add_item(stop_button)

        await ctx.send("Contrôles de la musique:", view=view)



    @commands.command()
    async def join(self, ctx: Context):
        try:
            channel_author = ctx.author.voice.channel.id
            channel_bot = ctx.channel.guild.me.voice.channel.id

            if channel_author == channel_bot:
                return ctx.send("je suis deja dans ton channel")
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


    @commands.command()
    async def test(self, ctx: Context):
        await ctx.author.voice.channel.connect()


    @commands.command()
    async def dis(self,ctx : Context):
        await ctx.voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(Play(bot))