from discord.ext import commands
import discord
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

class MyBot(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix="!", intents=discord.Intents.all())

  async def on_ready(self):
    print("Bot is ready!")

async def load_commands():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"commands.{filename[:-3]}")

async def load_event():
    for filename in os.listdir("./events"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"events.{filename[:-3]}")

bot = MyBot()



if __name__ == "__main__":
    asyncio.run(load_commands())
    asyncio.run(load_event())
    bot.run(TOKEN)