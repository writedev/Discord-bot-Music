from discord.ext import commands
import discord
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import string
import random

def generate_advanced_captcha():
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    image = Image.new('RGBA', (300, 100), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Ajout de motifs aléatoires
    for _ in range(50):
        x1, y1 = random.randint(0, 300), random.randint(0, 100)
        x2, y2 = random.randint(0, 300), random.randint(0, 100)
        draw.line((x1, y1, x2, y2), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255), width=2)

    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font = ImageFont.load_default()

    # Ajout de caractères avec rotation et distorsion
    for i, char in enumerate(captcha_text):
        x = 40 + i * 30
        y = random.randint(20, 50)
        char_image = Image.new('RGBA', (50, 50), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_image)
        char_draw.text((5, 5), char, font=font, fill=(0, 0, 0, 255))
        char_image = char_image.rotate(random.randint(-30, 30), expand=1)
        char_image = char_image.filter(ImageFilter.GaussianBlur(1))  # Ajout de flou
        image.paste(char_image, (x, y), char_image)

    # Application d'un léger bruit
    for _ in range(300):
        x, y = random.randint(0, 300), random.randint(0, 100)
        draw.point((x, y), fill=(0, 0, 0, random.randint(0, 255)))

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    
    return buffer, captcha_text

class Capcha(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        # Générer le captcha complexe
        captcha_image, captcha_text = generate_advanced_captcha()

        # Envoyer le captcha en message privé
        try:
            await member.send("Bienvenue sur le serveur! Veuillez résoudre ce captcha pour accéder au serveur.", file=discord.File(captcha_image, "captcha.png"))
            await member.send("Veuillez répondre avec le texte du captcha.")

            # Fonction de vérification de la réponse
            def check(m):
                return m.author == member and isinstance(m.channel, discord.DMChannel)

            # Attendre la réponse de l'utilisateur
            msg = await self.bot.wait_for("message", check=check, timeout=60.0)
            
            # Vérifier la réponse
            if msg.content.strip().upper() == captcha_text:
                role = discord.utils.get(member.guild.roles, name="Membre")
                if role:
                    await member.add_roles(role)
                    await member.send("Captcha réussi ! Bienvenue sur le serveur.")
            else:
                await member.send("Captcha incorrect. Veuillez réessayer en quittant et rejoignant le serveur.")
        except Exception as e:
            await member.guild.system_channel.send(f"{member.mention} n'a pas pu compléter le captcha à temps.")

async def setup(bot):
    await bot.add_cog(Capcha(bot))