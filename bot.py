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
    print('online')
for i in range(len(cogs)):
    cogs[i].setup(client)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client.run(token)