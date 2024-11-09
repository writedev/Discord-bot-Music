from discord.ext import commands
from discord import app_commands
import discord
from discord import ui

class ExplainButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()  

    @discord.ui.button(label="return",emoji="<:return_button:1303816930402238546>", style=discord.ButtonStyle.green)
    async def callback_return_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton retourne a la musique precedente", color=0xa6e712)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)

    @discord.ui.button(label="stop",emoji="<:stop_button:1303776558833467392>", style=discord.ButtonStyle.red)
    async def callback_stop_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton arrete la musique", color=0xa6e712)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)

    @discord.ui.button(label="pause",emoji="<:pause_button:1303776999864799313>", style=discord.ButtonStyle.green)
    async def callback_pause_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton met la musique en pause", color=0xa6e712)
        await interaction.response.send_message(embed=embed,ephemeral=True, delete_after=5)

    @discord.ui.button(label="skip ",emoji="<:skip_button:1303784286603972679>", style=discord.ButtonStyle.green)
    async def callback_skip_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton passe la musique suivante", color=0xa6e712)
        await interaction.response.send_message(embed=embed,ephemeral=True, delete_after=5)

    @discord.ui.button(label="Disable DJ mode",emoji="<:dj_button:1303814947242770436>", style=discord.ButtonStyle.red)
    async def callback_disable_autoplay_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton désactive le mode DJ ou active le mode DJ", color=0xa6e712)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)

    @discord.ui.button(label="volume",emoji="<:low_volume:1304587618947956749>", style=discord.ButtonStyle.green)
    async def callback_low_volume_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton diminue le sons de la musique de 10% sur 150%", color=0xa6e712)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)

    @discord.ui.button(label="volume",emoji="<:hight_volume:1304587386407227392>", style=discord.ButtonStyle.green)
    async def callback_high_volume_button(self, interaction : discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="Ce bouton augmente le sons de la musique de 10% sur 150%", color=0xa6e712)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)
    


class Play_command_explain_button(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def explain(self, ctx: commands.Context):
        view = ExplainButtonView()
        embed = discord.Embed(title="Explain button", description="clickez sur le bouton pour savoir son utilité", color=0xa6e712)
        embed.add_field(name="Dj mode",value="Le **mode DJ** est une option qui, lorsque la musique ou la playlist est terminée, continue de suggérer des morceaux.")
        await ctx.send(embed=embed, view=view)

async def setup(bot: commands.Bot):
    await bot.add_cog(Play_command_explain_button(bot))