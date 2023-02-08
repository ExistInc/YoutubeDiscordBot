import discord
import youtube_dl
import os

token = os.environ['token']
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content.startswith('!play'):
        # Get the URL of the YouTube video
        youtube_url = message.content[6:]
        
        # Use youtube_dl to extract the audio from the YouTube video
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(youtube_url, download=False)
            audio_url = video_info['url']

        # Join the voice channel and play the audio
        voice_channel = message.author.voice.channel
        voice = await voice_channel.connect()
        voice.play(discord.FFmpegPCMAudio(audio_url))
        while voice.is_playing():
            await asyncio.sleep(1)
        voice.stop()
        await voice.disconnect()

# Replace the placeholder token with your Discord bot token
client.run(token)
