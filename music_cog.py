from ast import alias
import discord
from discord.ext import commands
import random
from youtube_dl import YoutubeDL
#import tasks

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.list_of_admins = [127947460462116864]
        self.list_of_denied_users = [947566204309082112]
        self.list_of_denied_messages = ["Vous avez bien rejoint la boîte vocale de El Chapo. Veuillez laisser un message après le beep. *beep*",
                           "Le numéro composé n'est pas en service. Veuillez raccrocher et composer de nouveau. C'était un message enregistré.",
                           "Hello? Bye.", "You? Hmm... Maybe later.", "Password?", "Aaaanndd who are you exactly?", "https://shutupandtakemymoney.com/wp-content/uploads/2020/07/barack-obama-the-audacity-of-this-bitch-book-meme.jpg",
                           "Go play Rocket or som'n", "Sorry, YouTube is currently out of order. You can send a support ticket at youtube.com/fuckoff",
                           "I'm not playing this trash. K thx bye.", "Ooof, this is too trash for me.", "No.", "Ok, you are number 9347711 in queue.",
                           "Did you ask your momma first?", "How about YOU sing?", "Hello? I can't hear you, I'm deaf.", "Sorry... I am too stupid to fulfill that request.",
                           "Go on Spotify. Stoopid.", "Beep boop, I'm a bot.\nBeep boop, you're a cunt.", "I'm calling the police.", "I thought I was trash?",
                           "It's a bird! No, it's a plane! No, it's a denied request.", "01001110 01101111", "If you can read this, clap your hands.", "brb",
                           "Mmmmhh... No.", "Code it yourself.", "Beep boop, I'm a bot.\nBeep boop, suck a cock.", "Fuck off.", "Lezduit!", "Beep boop, I'm a bot.\nBeep boop, you're a slut.",
                           "Beep boop, I'm a bot.\nBeep boop, you're a thot.", "You've won... But at what cost?", "Processing request, please wait...", "Results came back...\nYou're a bitch.",
                           "Brb, let me go grab the milk.", "Fatal error occurred. Please note the following error code for future reference: \"Y0U-C4N-FUCK-0FF\".", "-500 social credit points.",
                           "https://cdnmetv.metv.com/z50xp-1619719725-16226-list_items-no.jpg", "http://images3.memedroid.com/images/UPLOADED58/5d426af598af9.jpeg","https://i.kym-cdn.com/photos/images/facebook/002/321/034/3b0.jpg",
                           "https://media.tenor.com/g-P8diB7FYgAAAAd/dont-care-didnt-ask-cope.gif","https://media.tenor.com/bT5vZjNhyt4AAAAC/sir-yes-sir-oorah-oorah.gif","https://media.tenor.com/hEgF0nc2rckAAAAC/uzui-better.gif",
                           "In order to use this bot, you will need to agree to the terms and conditions found at: https://discord.com/developers/applications", "https://open.spotify.com/", "https://www.youtube.com/premium",
                           "http://www.script-o-rama.com/movie_scripts/a1/bee-movie-script-transcript-seinfeld.html", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "https://www.linkedin.com/pulse/respect-software-engineers-rapha%C3%ABl-laffitte/"
                           ]
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
        # Block messages from list_of_denied_users
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
            print("Playing next song: " + self.music_queue[0][0]['title'])
            self.current_song = self.music_queue[0][0]['title']
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']
    
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)
            print("Playing: " + m_url)
            try:
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            except Exception as e:
                print(f"An error occurred during playback: {e}")
                self.is_playing = False
        else:
            self.is_playing = False


    async def play_music(self, ctx):
        if len(self.music_queue) == 0:
            await ctx.send("The queue is empty")
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
                print(f"An error occurred while connecting to the voice channel: {e}")
                self.reset()
                return
    
            if self.vc is None:
                await ctx.send("Could not connect to the voice channel.")
                print("Could not connect to the voice channel.")
                self.is_playing = False
                return
        else:
            try:
                await self.vc.move_to(voice_channel)
            except Exception as e:
                await ctx.send(f"An error occurred while moving to the voice channel: {e}")
                print(f"An error occurred while moving to the voice channel: {e}")
                self.is_playing = False
                return
    
        try:
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            print("Playing: " + m_url)
        except Exception as e:
            await ctx.send(f"An error occurred during playback: {e}")
            print(f"An error occurred during playback: {e}")
            await self.vc.disconnect()
            self.is_playing = False
            

    @commands.command(name="play", aliases=["p","playing"], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        print("Play command triggered by: " + str(ctx.author))
        if ctx.author.id in self.list_of_denied_users:
            random_message = random.choice(self.list_of_denied_messages)
            await ctx.send(random_message)
            return
        query = " ".join(args)

        #validate input
        if not query:
            await ctx.send("Please enter a search term.")
            await ctx.message.add_reaction("❌")
            return
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("You are not connected to a voice channel.")
            await ctx.message.add_reaction("❌")
            return

        # Check if the query is a url
        if "youtube.com" in query or "youtu.be" in query:
            try:
                # Download the song from the url
                with YoutubeDL(self.YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(query, download=False)
                song = {'source': info['formats'][0]['url'], 'title': info['title']}
                
            except Exception as e:
                await ctx.send(f"An error occurred while downloading the song: {e}")
                print(f"An error occurred while downloading the song: {e}")
                await ctx.message.add_reaction("❌")
                return
        else:
            # search for the song
            try:
                song = self.search_yt(query)
            except Exception as e:
                await ctx.send(f"An error occurred while searching for the song: {e}")
                print(f"An error occurred while searching for the song: {e}")
                await ctx.message.add_reaction("❌")
                return
        if type(song) == type(True):
            await ctx.send("Could not download the song. Incorrect format. Try another keyword or link. This can happen if you try to play a playlist, a livestream, an age-restricted video, or an unavailable video.")
            await ctx.message.add_reaction("❌")
            return
        else:
            await ctx.send("Adding song to queue: " + song['title'])
            await ctx.message.add_reaction("✅")
            self.music_queue.append([song, voice_channel])
            if self.is_paused:
                self.is_paused = False
                self.vc.resume()
            if not self.is_playing:
                try:
                    await self.play_music(ctx)
                except Exception as e:
                    await ctx.send(f"An error occurred while playing the song: {e}")
                    print(f"An error occurred while playing the song: {e}")
                    self.reset()

    @commands.command(name="pause", help="Pauses the current song being played")
    async def pause(self, ctx, *args):
        print("Pause command triggered by: " + str(ctx.author))
        if ctx.author.id in self.list_of_denied_users:
            random_message = random.choice(self.list_of_denied_messages)
            await ctx.send(random_message)
            return

        if self.is_playing:
            self.is_playing = True
            self.is_paused = True
            self.vc.pause()
            await ctx.send("Paused the song.")
            await ctx.message.add_reaction("⏸️")
        else:
            await ctx.send("Nothing is playing.")
            await ctx.message.add_reaction("❌")

    @commands.command(name = "resume", aliases=["r"], help="Resumes playing with the discord bot")
    async def resume(self, ctx, *args):
        print("Resume command triggered by: " + str(ctx.author))
        if ctx.author.id in self.list_of_denied_users:
            random_message = random.choice(self.list_of_denied_messages)
            await ctx.send(random_message)
            return
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
            await ctx.send("Resumed the song.")
            await ctx.message.add_reaction("▶️")
        else:
            await ctx.send("Nothing is paused.")
            await ctx.message.add_reaction("❌")

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        print("Skip command triggered by: " + str(ctx.author))
        if ctx.author.id in self.list_of_denied_users:
            random_message = random.choice(self.list_of_denied_messages)
            await ctx.send(random_message)
            return
        if self.is_playing:
            self.vc.stop()
            await ctx.send("Skipped the song.")
            await ctx.message.add_reaction("⏭️")
        
    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
    async def queue(self, ctx):
        print("Queue command triggered by: " + str(ctx.author))
        if ctx.author.id in self.list_of_denied_users:
            random_message = random.choice(self.list_of_denied_messages)
            await ctx.send(random_message)
            return
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display all the songs in the queue with their index
            retval += str(i+1) + ": " + self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")
            await ctx.message.add_reaction("❌")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
    async def clear(self, ctx):
        print("Clear command triggered by: " + str(ctx.author))
        if ctx.author.id in self.list_of_denied_users:
            random_message = random.choice(self.list_of_denied_messages)
            await ctx.send(random_message)
            return     
        try:
            self.vc.stop()
        except:
            pass
        await ctx.send("Cleared the queue")
        await ctx.message.add_reaction("🗑️")
        self.reset()

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        print("Leave command triggered by: " + str(ctx.author))
        if ctx.author.id in self.list_of_denied_users:
            random_message = random.choice(self.list_of_denied_messages)
            await ctx.send(random_message)
            return
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
        await ctx.send("Disconnected from voice channel")
        await ctx.message.add_reaction("👋")
    
    @commands.command(name="nowplaying", aliases=["np"], help="Displays the current song being played")
    async def nowplaying(self, ctx):
        print("Nowplaying command triggered by: " + str(ctx.author))
        if ctx.author.id in self.list_of_denied_users:
            random_message = random.choice(self.list_of_denied_messages)
            await ctx.send(random_message)
            return
        if self.is_playing:
            await ctx.send("Now playing: " + self.current_song)
            await ctx.message.add_reaction("🎶")
        else:
            await ctx.send("No song is currently playing.")
            await ctx.message.add_reaction("❌")

    @commands.command(name="stop" , help="Stops the music.")
    async def stop(self, ctx):
        print("Stop command triggered by: " + str(ctx.author))
        if ctx.author.id in self.list_of_denied_users:
            random_message = random.choice(self.list_of_denied_messages)
            await ctx.send(random_message)
            return
        if self.is_playing:
            self.vc.stop()
            await ctx.send("Stopped the song.")
            await ctx.message.add_reaction("⏹️")
            self.reset()
        else:
            await ctx.send("No song is currently playing.")
            await ctx.message.add_reaction("❌")

    @commands.command(name="ping", help="Displays the current ping of the bot")
    async def ping(self, ctx):
        print("Ping command triggered by: " + str(ctx.author))
        if ctx.author.id in self.list_of_denied_users:
            random_message = random.choice(self.list_of_denied_messages)
            await ctx.send(random_message)
            return
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')
        await ctx.message.add_reaction("🏓")

    @commands.command(name="license", help="Displays the license of the bot")
    async def license(self, ctx):
        print("License command triggered by: " + str(ctx.author))
        if ctx.message.author.id == 127947460462116864:
            await ctx.send("You are the owner of this bot, you already know the license.")
            await ctx.message.add_reaction("👍")
        else:
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
            await ctx.message.add_reaction("📜")
        

    def reset(self):
        print("Resetting variables")
        # disconnect
        self.vc.stop()
        self.vc.disconnect()
        # reset the variables
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.vc = None
        self.current_song = None

    @commands.command(name="reset", help="Resets the bot")
    async def reset(self, ctx):
        print("Reset command triggered by: " + str(ctx.author))
        if ctx.message.author.id in self.list_of_denied_users:
            random_message = random.choice(self.list_of_denied_messages)
            await ctx.send(random_message)
            return
        try:
            # disconnect
            self.vc.stop()
            await self.vc.disconnect()
            # reset the variables
            self.is_playing = False
            self.is_paused = False
            self.music_queue = []
            self.vc = None
            self.current_song = None
            await ctx.send("I should be reset now. If there are still problems, try doing #leave, #clear and #stop. If that doesn't work, contact: <@!127947460462116864> with information about what happened.")
            await ctx.message.add_reaction("🔄")
        except:
            await ctx.send("I was unable to fully reset. Please contact: <@!127947460462116864> with information about what happened. Meanwhile, try doing #leave, #clear and #stop.")
            await ctx.message.add_reaction("❌")

    #############################
    #   Admin commands          #
    #############################

    @commands.command(name="ban", help="Deny a user from using the bot")
    async def ban(self, ctx, user: discord.User):
        print("Ban command triggered by: " + str(ctx.author))
        if ctx.message.author.id in self.list_of_admins:
            self.list_of_denied_users.append(user.id)
            await ctx.send("Banned " + str(user) + " from using the bot.")
            await ctx.message.add_reaction("👍")
        else:
            await ctx.send("You are not allowed to use this command.")
            await ctx.message.add_reaction("❌")

    @commands.command(name="unban", help="Allow a user to use the bot")
    async def unban(self, ctx, user: discord.User):
        print("Unban command triggered by: " + str(ctx.author))
        if ctx.message.author.id in self.list_of_admins:
            try:
                self.list_of_denied_users.remove(user.id)
                await ctx.send("Unbanned " + str(user) + " from using the bot.")
                await ctx.message.add_reaction("👍")
            except:
                await ctx.send("User is not banned.")
                await ctx.message.add_reaction("❌")
        else:
            await ctx.send("You are not allowed to use this command.")
            await ctx.message.add_reaction("❌")
    @commands.command(name="listbanned", help="List all banned users")
    async def listbanned(self, ctx):
        print("Listbanned command triggered by: " + str(ctx.author))
        if ctx.message.author.id in self.list_of_admins:
            await ctx.send("Banned users: " + str(self.list_of_denied_users))
            await ctx.message.add_reaction("��")
        else:
            await ctx.send("You are not allowed to use this command.")
            await ctx.message.add_reaction("❌")
    
    @commands.command(name="say", help="Make the bot say something")
    async def say(self, ctx, *, message):
        print("Say command triggered by: " + str(ctx.author))
        if ctx.message.author.id in self.list_of_admins:
            await ctx.send(message)
            # delete the command message
            await ctx.message.delete()
        else:
            await ctx.send("You are not allowed to use this command.")
            await ctx.message.add_reaction("❌")
    

