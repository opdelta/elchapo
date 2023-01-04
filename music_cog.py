from ast import alias
import discord
from discord.ext import commands

from youtube_dl import YoutubeDL
#import tasks
class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.current_song = None
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

        self.minutesalone = 0

        self.client = bot
     #searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
    
            #get the first url
            m_url = self.music_queue[0][0]['source']
    
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)
    
            try:
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            except Exception as e:
                print(f"An error occurred during playback: {e}")
                self.is_playing = False
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self, ctx):
        if len(self.music_queue) == 0:
            self.is_playing = False
            return
    
        self.is_playing = True
        self.current_song = self.music_queue[0][0]['title']
        m_url = self.music_queue[0][0]['source']
        voice_channel = self.music_queue[0][1]
        self.music_queue.pop(0)
        
    
        # Connect to voice channel if not already connected
        if self.vc is None or not self.vc.is_connected():
            try:
                self.vc = await voice_channel.connect()
            except Exception as e:
                await ctx.send(f"An error occurred while connecting to the voice channel: {e}")
                self.is_playing = False
                return
    
            if self.vc is None:
                await ctx.send("Could not connect to the voice channel")
                self.is_playing = False
                return
        else:
            try:
                await self.vc.move_to(voice_channel)
            except Exception as e:
                await ctx.send(f"An error occurred while moving to the voice channel: {e}")
                self.is_playing = False
                return
    
        try:
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        except Exception as e:
            await ctx.send(f"An error occurred during playback: {e}")
            self.is_playing = False

    @commands.command(name="play", aliases=["p","playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)

        # Validate input
        if not query:
            await ctx.send("Please provide a search query.")
            return

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
            return

        # Search YouTube
        try:
            song = self.search_yt(query)
        except Exception as e:
            await ctx.send(f"An error occurred while searching YouTube: {e}")
            return

        if type(song) == type(True):
            await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            return
        else:
            await ctx.send("Song added to the queue")
            self.music_queue.append([song, voice_channel])

            if self.is_paused:
                self.vc.resume()
                return
            elif not self.is_playing:
                # Play music
                try:
                    await self.play_music(ctx)
                except Exception as e:
                    await ctx.send(f"An error occurred during playback: {e}")
                    self.is_playing = False
                    self.vc = None
                    self.music_queue = []

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
            await ctx.send("Paused the song.")
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            await ctx.send("Resumed the song.")

    @commands.command(name = "resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            await ctx.send("Resumed the song.")

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            try:
                await self.play_music(ctx)
                await ctx.send("Skipped the song and playing the next one in queue: " + self.current_song['title'])
            except Exception:
                await ctx.send("No more songs in queue")
                self.is_playing = False
                self.is_paused = False
        else:
            await ctx.send("No song is currently playing.")



    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")
        self.is_playing = False
        self.is_paused = False
        self.current_song = None

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
        await ctx.send("Disconnected from voice channel")
    
    @commands.command(name="nowplaying", aliases=["np"], help="Displays the current song being played")
    async def nowplaying(self, ctx):
        if self.is_playing:
            await ctx.send("Now playing: " + self.current_song)
        else:
            await ctx.send("No song is currently playing.")

    @commands.command(name="stop" , help="Stops the music and clears the queue")
    async def stop(self, ctx):
        self.clear(ctx)
        self.is_playing = False
        self.is_paused = False
        await ctx.send("Music stopped")

    @commands.command(name="ping", help="Displays the current ping of the bot")
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(name="license", help="Displays the license of the bot")
    async def license(self, ctx):
        await ctx.send("""
        ```
        MIT License
        
        copyright (c) 2023-2024 Ziad Lteif

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:
        
        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
        ```
        """
        )
