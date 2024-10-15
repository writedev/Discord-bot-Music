from discord.ext import commands
import discord

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="!")

@bot.command()
async def ping(ctx):
  await ctx.send("Pong!")


bot.run("MTI1Mjk5Njc2NTU1NzE5NDgyMg.GxV8f7.Wsj3MsrQgymE5Iv1YaJiww6T6AUMDBe4-b2xlg")