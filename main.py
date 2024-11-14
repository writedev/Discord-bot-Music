from discord.ext import commands
import discord
import logging
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


# bot part

class MyBot(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix="!", intents=discord.Intents.all())

  async def on_ready(self):
    print("Bot is ready!")
    await self.tree.sync()

# loading folder part

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

# start of bot part

if __name__ == "__main__":
    asyncio.run(load_commands())
    asyncio.run(load_event())
    bot.run(token=TOKEN, log_handler=handler, log_level=logging.DEBUG)