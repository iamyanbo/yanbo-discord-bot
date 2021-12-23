from os import stat
import time
import discord
from discord.errors import ClientException
from discord.ext import commands
import youtube_dl
import asyncio

class music(commands.Cog):
    def __init__(self, client):
        self.client = client 
        self.queue = {}
        self.client.remove_command('help')
    @commands.command()
    async def help(self, ctx):
        await ctx.channel.send('```i am bot, beep boop \nplay youtube sing: .play [url]\
            \nfind where people are: .where [person]```')
    
    @commands.command()
    async def wheres(self, ctx, message):
        if message.lower() == "ryan":
            user = '<@!361913675872731136>'
            await ctx.channel.send(f'{user} downstairs showering with his bri\'ish cousins playing csgo and eating and taking a LGBTQ poop')
        if message.lower() == 'john':
            user = '<@432949846991831040>'
            await ctx.channel.send(f'{user} is ganked 😂🤣😔😴💀')
        if message.lower() == 'marcus':
            user = '<@!516624806515572737>'
            await ctx.channel.send(f'{user} is buying stone swords again... 😭🤢🤢🤢😰')
        if message.lower() == 'yanbo':
            user ='<@207568895156944896>'
            await ctx.channel.send(f'{user} is being the better brother and probs doing nothing rn cus he is lazy')
        if message.lower() == 'timothy' or message.lower() == 'timmy':
            user ='<@!194955178770825216>'
            await ctx.channel.send(f'{user} is being sus')
        
            
    @commands.command()
    async def join(self, ctx):
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else: 
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def dc(self, ctx):
        await ctx.voice_client.disconnect()
           
    
            
            
    @commands.command()
    async def play(self, ctx, url):
        voice_channel = ctx.author.voice.channel
        server = ctx.message.guild
        if server.id not in self.queue:
            self.queue[server.id] = [url]
        else:
            self.queue[server.id].append(url)
        if ctx.voice_client is None:
            await voice_channel.connect()
        else: 
            await ctx.voice_client.move_to(voice_channel)
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
        }
        
        YDL_OPTIONS = {
            'format' :'bestaudio',
            'forceduration': True
        }
        vc = ctx.voice_client
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            duration = int(info['duration']) + 1
            print(duration)
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            try:
                vc.play(source, after=lambda e:asyncio.run(check_queue(self, ctx, server.id)))
            except ClientException:
                pass           
async def check_queue(self, ctx, id):
        if self.queue[id] != []:
            print(self.queue[id])
            print('-------------------------------------')
            a=self.queue[id].pop(0)
            vc = ctx.voice_client
            FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
            }
        
            YDL_OPTIONS = {
            'format' :'bestaudio',
            'forceduration': True
            }
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(self.queue[id][0], download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                
                try:
                    vc.play(source, after=lambda e:asyncio.run(check_queue(self, ctx, id)))
                except ClientException:
                    pass 
                
def setup(client):
    client.add_cog(music(client))
