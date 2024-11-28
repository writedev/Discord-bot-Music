import discord
from discord.ext import commands
from discord.ext.commands import Context
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

class Search(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="search", aliases=["s"])
    async def search(self,ctx, *, query):
        # Recherche de chansons via Wavelink
        tracks = await wavelink.Playable.search(query)

        if not tracks:
            await ctx.send("Aucun résultat trouvé pour votre recherche.")
            return

        # Envoie un menu déroulant pour sélectionner une chanson
        await ctx.send("🎶 Sélectionnez une chanson :", view=SearchMenu(tracks, ctx))

async def setup(bot : commands.Bot):
    await bot.add_cog(Search(bot))