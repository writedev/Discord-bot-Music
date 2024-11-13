from discord.ext import commands
import discord
from discord import ui

class ExplainButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()  

    # button return

    @discord.ui.button(label="return (explain)",emoji="<:return_button:1303816930402238546>", style=discord.ButtonStyle.green)
    async def callback_return_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton retourne a la musique precedente", color=0xa6e712)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)
    
    # button stop

    @discord.ui.button(label="stop (explain)",emoji="<:stop_button:1303776558833467392>", style=discord.ButtonStyle.red)
    async def callback_stop_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton arrete la musique", color=0xa6e712)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)

    # button pause

    @discord.ui.button(label="pause(explain)",emoji="<:pause_button:1303776999864799313>", style=discord.ButtonStyle.green)
    async def callback_pause_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton met la musique en pause", color=0xa6e712)
        await interaction.response.send_message(embed=embed,ephemeral=True, delete_after=5)

    # button skip

    @discord.ui.button(label="skip (explain)",emoji="<:skip_button:1303784286603972679>", style=discord.ButtonStyle.green)
    async def callback_skip_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton passe a la musique suivante", color=0xa6e712)
        await interaction.response.send_message(embed=embed,ephemeral=True, delete_after=5)

    # button autoplay

    @discord.ui.button(label="DJ mode (explain)",emoji="<:dj_button:1303814947242770436>", style=discord.ButtonStyle.primary)
    async def callback_disable_autoplay_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton désactive le mode DJ ou active le mode DJ", color=0xa6e712)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)
    
    # button low volume

    @discord.ui.button(label="volume (explain)",emoji="<:low_volume:1304587618947956749>", style=discord.ButtonStyle.green)
    async def callback_low_volume_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton diminue le sons de la musique de 10% sur 150%", color=0xa6e712)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)

    # button high volume

    @discord.ui.button(label="volume (explain)",emoji="<:hight_volume:1304587386407227392>", style=discord.ButtonStyle.green)
    async def callback_high_volume_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton augmente le sons de la musique de 10% sur 150%", color=0xa6e712)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)
    


class Play_command_explain_button(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(aliases=["music_explain"])
    async def explain_play_button(self, ctx: commands.Context):
        view = ExplainButtonView()
        embed = discord.Embed(title="Explain button", description="clickez sur le bouton pour savoir son utilité", color=0xa6e712)
        embed.add_field(name="Dj mode",value="Le **mode DJ** est une option qui, lorsque la musique ou la playlist est terminée, continue de suggérer des morceaux.")
        # self du message pour envoyer pour suppr dans play commands
        await ctx.send(embed=embed, view=view, ephemeral=True, delete_after=10)

async def setup(bot: commands.Bot):
    await bot.add_cog(Play_command_explain_button(bot))