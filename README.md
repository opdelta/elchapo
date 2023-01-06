# El Chapo Music Bot
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

ElChapo is a private Discord music bot that allows a small Discord community to 
listen to music together (personal uses only). It is a simple bot programmed in Python3. 

ElChapo has multiple features that allows users to playback, pause, stop, 
add music to queue, etc.



## Author(s)

- [opdelta](https://www.github.com/opdelta)


## Installation and deployment

### Prerequisites
In order for the bot to work, you will need the following:

- Python 3.8 or better. (Versions below Python 3.8 have not been tested. Python 2 **IS NOT** supported).
- pip 20.0.2 or better.
- Docker 20.10.21 or better.

You will also need to create a Discord bot using the Discord developer console (https://discord.com/developers/applications).


### Docker deployement

First of all, you will need to run:

`docker build -t "elchapo:latest" .`

This command will create an image called `elchapo` with the version being `latest`
allowing you to run this docker image in a container.

You can run the docker container by running the following command:

`docker run --env DISCORD_TOKEN=Y0uR_T0k3N elchapo:latest`

Your bot should be online and working on your discord server.


## Environment Variables

To run this project, you will need to add the following environment variables to your Docker container

`DISCORD_TOKEN`

If you do not wish to use environment variables, `the bot.run()` will need to be passed in your token in parameters instead of the `os.getenv()`.



## License

[MIT](https://choosealicense.com/licenses/mit/)


## Documentation

```
El Chapo music bot developped by opdelta for personal use only.
Commands:
#help - Displays this message
#play <song name> - Plays a song from YouTube
#pause - Pauses the current song
#resume - Resumes the current song
#stop - Stops the current song
#skip - Skips the current song
#remove <number> - Removes a song from the queue
#queue - Displays the current queue
#clear - Clears the current queue
#shuffle - Shuffles the current queue
#leave - Leaves the voice channel
#move <number> <number> - Moves a song in the queue
#ping - Pong!
#license - Displays the license
```