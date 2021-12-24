import os
import discord
from discord import channel
from discord.channel import VoiceChannel
from dotenv import load_dotenv 
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
import music
import asyncio
cogs = [music]

client = commands.Bot(command_prefix = '.')
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='The Boys .help'))
    print('asdf')
for i in range(len(cogs)):
    cogs[i].setup(client)



client.run('OTIyOTgxMzUyNjI0NzY3MDE3.YcJXXg.g3og56O-DIA5Q3ppYljdsfntCo8')
"""@client.command(pass_context = True)
async def play(ctx, url: str):
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
    except PermissionError:
        await ctx.send('wait, im playing rn, or use stop command')
        return 
    
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = 'General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)


        
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio('song.mp3'))
    

@client.command()
async def leave(ctx):
        voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send('lmao u kinda retarded eh?')

@client.command()
async def pause(ctx):
        voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send('im not even playing')

@client.command()
async def resume(ctx):
        voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send('im already playing')

@client.command
async def stop(ctx):
        voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
        voice.stop()
@client.event
async def on_ready():
    print(f'{client.user} has connected, hehexd')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$hi"):
        await message.channel.send('hi')
"""
