import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.help_message = """
        ```
        El Chapo music bot developped by opdelta for personal use only.
        Commands:
        #help - Displays this message
        #play <song name> - Plays a song from YouTube
        #pause - Pauses the current song
        #resume - Resumes the current song
        #stop - Stops the current song
        #skip - Skips the current song
        #queue - Displays the current queue
        #clear - Clears the current queue
        #leave - Leaves the voice channel
        #reset - Resets the bot
        #ping - Pong!
        #license - Displays the license

        Should you encounter any bugs, please report them to opdelta#1665 on Discord with as much information as possible about the bug.
        ```
        """
        self.text_channel_text = []

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.channels:
                if type(channel) == discord.channel.TextChannel:
                    #self.text_channel_text.append(channel)
                    continue

        #await self.send_to_all(self.help_message)

    @commands.command(name='help', help='Displays this message')
    async def help(self, ctx):
        await ctx.send(self.help_message)
        print("Help command executed by " + str(ctx.author) + " in " + str(ctx.channel) + " at " + str(ctx.message.created_at) + " UTC")

    async def send_to_all(self, message):
        for channel in self.text_channel_text:
            await channel.send(message)

    
    
