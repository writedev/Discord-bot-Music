from discord.ext import commands
import discord
from discord.ui import Button, View

class Utils(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    async def ping(self, ctx : commands.Context):
        ping = round(self.bot.latency * 1000)

        button = discord.ui.Button(label="Ping ",emoji="<:cable:1303389854561996900>", style=discord.ButtonStyle.primary, custom_id="ping")
        view = discord.ui.View()
        view.add_item(button)

        async def ping_bouton(interaction : discord.Interaction):
            await interaction.response.send_message(f"Pong! {ping}ms")
        
        button.callback = ping_bouton
        await ctx.send(f"Pong! {ping}ms", view=view, ephemeral=True)

    @commands.command()
    async def test(self, ctx : commands.Context):
        embed = discord.Embed(title=f"@{ctx.author.name}")
        await ctx.send(embed=embed)

"""    @commands.command()
    async def bouton(self,ctx):
        # Création du bouton initial
        bouton = Button(label="Clique moi", style=discord.ButtonStyle.primary)

        async def on_click(interaction):
            # Changer le label du bouton après le clic
            bouton.label = "Je suis cliqué"
            bouton.style = discord.ButtonStyle.success
            bouton.callback = on_click_2  # Optionnel : changer la couleur pour indiquer l'état cliqué

            # Rééditer le message avec le nouveau label du bouton
            await interaction.message.edit(view=view)
            await interaction.response.send_message("Bouton cliqué !", ephemeral=True)

        async def on_click_2(interaction : discord.Interaction):
            bouton.label = "click me"
            bouton.style = discord.ButtonStyle.primary  # Optionnel : changer la couleur pour indiquer l'état cliqué
            await interaction.response.send_message("Bouton cliqué !", ephemeral=True)
            await interaction.message.edit(view=view)
            bouton.callback = on_click
        bouton.callback = on_click
        view = View()
        view.add_item(bouton)
        await ctx.send("Voici un bouton :", view=view)
""" 
async def setup(bot):
    await bot.add_cog(Utils(bot))