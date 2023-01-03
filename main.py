import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from help_cog import help_cog
from music_cog import music_cog

load_dotenv()
bot = commands.Bot(command_prefix='#')
bot.remove_command("help")
bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))

bot.run(os.getenv('DISCORD_TOKEN'))