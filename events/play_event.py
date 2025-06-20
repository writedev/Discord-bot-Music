from discord.ext import commands
import discord
from discord.ext.commands import Context
import discord.voice_state
import wavelink


class PlayEvent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload):
        print(payload.track.title)

async def setup(bot):
    await bot.add_cog(PlayEvent(bot)) 