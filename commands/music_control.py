from discord.ext import commands
from discord.ext.commands import Context
import discord
from typing import cast
import wavelink
from datetime import timedelta

class SearchMenu(discord.ui.View):
    def __init__(self, tracks, ctx):
        super().__init__(timeout=60)
        self.tracks = tracks
        self.ctx = ctx

        # Ajoute les chansons comme options du menu déroulant
        options = [
            discord.SelectOption(
                label=track.title[:100],
                description=f"{track.author}",
                value=str(i),
            )
            for i, track in enumerate(tracks[:10])  # Limite à 10 résultats
        ]
        self.add_item(SearchSelect(options, tracks, ctx))


class SearchSelect(discord.ui.Select):
    def __init__(self, options, tracks, ctx):
        super().__init__(placeholder="Sélectionnez une chanson...", options=options)
        self.tracks = tracks
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        # Récupère la chanson sélectionnée
        selected_track = self.tracks[int(self.values[0])]

        # Envoie le titre et le lien dans le canal texte
        await interaction.response.send_message(f"[{selected_track.title}]({selected_track.uri})", ephemeral=False)


class MusiqueControl(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.history = {}

    @commands.hybrid_command(aliases=["info_music", "play_info"])
    async def music_info(self, ctx: Context):
        try:
            player : wavelink.Player
            player = cast(wavelink.Player, ctx.voice_client)
            # calcul time of music and position
            duration = str(timedelta(milliseconds=player.current.length))
            music_image = player.current.artwork
            # music info
            music_title= f"`{player.current.title}`"
            music_author = f"`{player.current.author}`"
            # ajout dans l'embed
            embed = discord.Embed(color=discord.Color.blue() )
            embed.set_thumbnail(url=music_image)
            embed.add_field(name="Titre ✨", value=f"`{music_title}`", inline=True) #music_title, inline=False)
            embed.add_field(name="Auteur ✍️", value=music_author, inline=True)
            embed.add_field(name="Durée 🕰️", value=f"`{duration}`", inline=False)
            embed.add_field(name="Volume 🔊", value=f"`{player.volume}%`", inline=True)
            embed.add_field(name="URL 🔗", value=f"[Cliquez ici]({player.current.uri})", inline=False)
            await ctx.send(embed=embed, ephemeral=True, delete_after=15)
        except AttributeError:
            embed = discord.Embed(description="❌ aucune musique est en cours", color=discord.Color.blue())
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)

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
                activate_dj_mode_commande = f"</explain_active_dj_mode:{1307300357122162700}>"
                embed = discord.Embed(description="❌ Active le dj mode",color=discord.Color.blue())
                embed.add_field(name="tuto active le dj mode ", value=activate_dj_mode_commande)
                await ctx.send(embed=embed, ephemeral=True, delete_after=5)
            elif not player.queue.is_empty:
                await player.skip()
            elif player.autoplay == wavelink.AutoPlayMode.enabled:
                await player.skip(force=True)
                embed = discord.Embed(description=f"✅The track **{player.current.title}** by **{player.current.author}** has been skipped.", color=discord.Color.blue())
                await ctx.send(embed=embed, ephemeral=True, delete_after=5)
        else:
            embed = discord.Embed(description="❌ Nothing is currently playing.",color=discord.Color.blue())
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)

    @commands.hybrid_command(name="volume", aliases=["v"])
    async def change_volume(self, ctx: Context, percentage: int):
        player: wavelink.Player = ctx.guild.voice_client
        if percentage > 150:
            percentage = 150
        elif percentage < 0:
            percentage = 0
        if player and player.playing == True:
            await player.set_volume(percentage)
            embed = discord.Embed(title=f"Volume has been changed to {percentage}% ✅", color=discord.Color.blue())
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)
        else:
            embed = discord.Embed(description="❌ Nothing is currently playing.",color=discord.Color.blue())
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)

    @commands.hybrid_command(name="stop")
    async def stop(self, ctx: Context):
        player: wavelink.Player = ctx.guild.voice_client
        if player and player.playing == True:
            await player.stop()
            embed = discord .Embed(description="The player has been stopped ✅",color=discord.Color.blue())
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)
        else:
            embed = discord .Embed( description="❌ Nothing is currently playing.",color=discord.Color.blue())
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)

    @commands.hybrid_command(name="disconnect", aliases=["dc","dis"])
    async def disconnect(self, ctx: Context):
        if ctx.voice_client:
            await ctx.voice_client.disconnect(force=True)
            embed = discord.Embed(description="The player has been disconnected ✅",color=discord.Color.blue())
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)
        else:
            embed = discord.Embed(description="❌ Nothing is currently connected.",color=discord.Color.blue())
            await ctx.send(embed=embed, ephemeral=True, delete_after=5)


    @commands.hybrid_command(name="explain_active_dj_mode")
    async def explain_active_dj_mode(self, ctx: Context):
        embed = discord.Embed(title="Explain active dj mode 📖", color=discord.Color.blue())
        embed.set_image(url="https://i.imgur.com/PwLhatP.png")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_wavelink_track_start(self,payload: wavelink.TrackStartEventPayload):
        guild_id = payload.player.guild.id
        if guild_id not in self.history:
            self.history[guild_id] = []
        # Ajoute un tuple (titre, URL) à l'historique
        self.history[guild_id].append((payload.track.title, payload.track.uri))

        # Limite l'historique à 10 chansons par défaut
        if len(self.history[guild_id]) > 10:
            self.history[guild_id].pop(0)

    @commands.hybrid_command()
    async def history(self,ctx : commands.Context):
        guild_id = ctx.guild.id
        if guild_id not in self.history or len(self.history[guild_id]) == 0:
            await ctx.send("Aucune chanson dans l'historique.")
            return

        # Formater l'historique en message
        description = "\n".join(
            f"{i + 1}. [{title}]({url})" for i, (title, url) in enumerate(self.history[guild_id])
        )
        embed = discord.Embed(
            title="Historique des chansons jouées",
            description=description,
            color=discord.Color.blue(),
        )
        await ctx.send(embed=embed)

"""    @commands.command(name="search")
    async def search(self, ctx : commands.Context, *, query: str):
        Searches for tracks and allows the user to select one.
        tracks = await wavelink.Playable.search(query)

        if not tracks:
            await ctx.send("No results found.")
            return

        # Crée une liste d'options pour le menu Select avec numérotation
        options = [
            discord.SelectOption(
                label=f"{i + 1}. {track.title[:90]}",  # Limite à 90 caractères pour éviter des dépassements
                description=f"{track.author}",
                value=str(i)  # Utiliser l'index comme valeur
            )
            for i, track in enumerate(tracks[:10])  # Limiter à 10 résultats
        ]

        # Créer le menu déroulant (Select)
        select = discord.ui.Select(placeholder="Choose a track", options=options)

        async def select_callback(interaction : discord.Interaction):
            # Récupérer la piste sélectionnée
            index = int(select.values[0])
            selected_track = tracks[index]

            # Se connecter au canal vocal et jouer la piste
            if not ctx.author.voice or not ctx.author.voice.channel:
                await interaction.response.send_message("Vous devez être dans un canal vocal pour jouer de la musique.", ephemeral=True)
                return
            await Play.play(ctx, query=selected_track.uri)
            

        select.callback = select_callback

        # Envoyer l'embed avec la liste des pistes et le menu déroulant
        embed = discord.Embed(title="Pick a track you want to queue", color=discord.Color.blurple())
        embed.description = "\n".join(
            [f"**``{i + 1}.``**      **``{str(timedelta(milliseconds=track.length))}``**       **[{track.title}]({track.uri})** " for i, track in enumerate(tracks[:10])]
        )
        view = discord.ui.View()
        view.add_item(select)
        await ctx.send(embed=embed, view=view)"""


# search commande 

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