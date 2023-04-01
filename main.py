#!/usr/bin/python3
import discord
from discord.ext import commands
import os
from help_cog import help_cog
from music_cog import music_cog

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='#', intents=intents)
bot.remove_command("help")
print("Bot is starting")
async def setup():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))
    print("Bot is ready")
    channel = bot.get_channel(1054511536384774204)
    await channel.send("I just woke up! Sup?")

bot.add_listener(setup, "on_ready")
bot.run(os.getenv("DISCORD_TOKEN"))