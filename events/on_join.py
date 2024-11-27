import discord
from discord.ext import commands
from discord.ext.commands import Context
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string
import io
import asyncio

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

async def welcome_message(member: discord.Member, welcome_channel: discord.TextChannel):
    embed = discord.Embed(
        title="Captcha reussi ! ✅",
        description=f"⬇️ Garde cela au chaud pour ne jamais l'oublier ! ⬇️",
        color=discord.Color.blue(),
    )
    await member.send(embed=embed)
    await member.send(await welcome_channel.create_invite())
    welcome_embed = discord.Embed(
        title="🎉 Bienvenue sur le serveur !",
        description=f"{member.mention} a rejoint le serveur !",
        color=discord.Color.blue(),
    )
    await welcome_channel.send(embed=welcome_embed)

class OnJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_channel = self.bot.get_channel(1311390806589837353)

        captcha_image, captcha_text = generate_advanced_captcha()

        # Envoyer le captcha en message privé
        try:
            captcha_embed = discord.Embed(title="🎉 Bienvenue sur le serveur!", description=f"**Veuillez résoudre ce captcha pour accéder au serveur integralement a {member.guild.name}**", color=discord.Color.blue())
            file = discord.File(fp=captcha_image, filename="captcha.png")
            captcha_embed.set_image(url="attachment://captcha.png")
            captcha_message = await member.send(file=file, embed=captcha_embed)

            # Fonction de vérification de la réponse
            def check(m):
                return m.author == member and isinstance(m.channel, discord.DMChannel)

            attempts = 2
            for attempt in range(attempts):
                try:
                    # Attendre la réponse de l'utilisateur
                    msg = await self.bot.wait_for("message", check=check, timeout=40.0)

                    # Vérifier la réponse
                    if msg.content.strip().upper() == captcha_text:
                        role = discord.utils.get(member.guild.roles, name="Membre")
                        if role:
                            await member.add_roles(role)
                            # Supprimer les messages envoyés par le bot
                            await captcha_message.delete()
                            await welcome_message(member, welcome_channel)
                            return
                    else:
                        await member.send(f"❌ Captcha incorrect. Il vous reste **`{attempts - attempt - 1}`** tentative(s).")
                except asyncio.TimeoutError:
                    embed_timeout = discord.Embed(description=f"❌ Temps écoulé. Il vous reste **`{attempts - attempt - 1}`** tentative(s).", color=discord.Color.blue())
                    await member.send(embed=embed_timeout)

            embed_expulsion = discord.Embed(description="❌ Vous avez atteint le nombre maximum d'essais. Vous allez étre expulsé du serveur.", color=discord.Color.blue())
            await captcha_message.delete()
            await member.send(embed=embed_expulsion)
            await member.kick()
        except Exception as e:
            embed = discord.Embed(description=f"❌ Une erreur s'est produite {e}", color=discord.Color.blue())
            await member.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(OnJoin(bot))
