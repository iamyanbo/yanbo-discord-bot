from os import stat
import time
import discord
from discord.errors import ClientException
from discord.ext import commands
import youtube_dl
import asyncio
import pandas

from youtube_dl.YoutubeDL import YoutubeDL
import validators

class music(commands.Cog):
    def __init__(self, client):
        self.client = client 
        self.queue = {}
        self.client.remove_command('help')
        self.queue_name = {}
    @commands.command(name='help', aliases=['commands'])
    async def help(self, ctx):
        await ctx.channel.send('```i am bot, beep boop \nplay youtube sing: .play [url]\
            \nfind where people are: .where [person]\n.skip to skip current song```')
    
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
            await ctx.channel.send(f'{user} is being sus, pause')

    @commands.command(name='dc', aliases=['disconnect'])
    async def dc(self, ctx):
        vc = ctx.voice_client
        vc.stop()
        await ctx.voice_client.disconnect()
        server = ctx.message.guild
        self.queue_name[server.id] = []
        self.queue[server.id] = []
                    
    @commands.command()
    async def play(self, ctx, *message):
        try:
            voice_channel = ctx.author.voice.channel
        except:
            await ctx.channel.send('ur not in a vc dumbo')
            return
        if message == ():
            await ctx.channel.send('you are playing nothing dumbo')
            return 
        url = ' '.join(message)
        
        server = ctx.message.guild
        if ctx.voice_client is None:
            await voice_channel.connect()
        else: 
            await ctx.voice_client.move_to(voice_channel)
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
            'options': '-vn'
        }
        
        YDL_OPTIONS = {
            'default_search': 'auto',
            'format' :'--no-playlist, bestaudio',
            'forceduration': True,
            'noplaylist': True
        }
        vc = ctx.voice_client
        if validators.url(url):
            if 'list' in url:
                #make this a seperate function tmr
                #and make sure the reaction only takes the first one, subsequent reactions will not count
                
                print('playlist')
                msg = await ctx.channel.send('this is a playlist, do you want to play the whole thing?')
                await msg.add_reaction('👍')
                await msg.add_reaction('👎')
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=60, check=lambda reaction, user: reaction.emoji in ['👍','👎'] and user == ctx.message.author)
                    await msg.remove_reaction(reaction.emoji, user)
                except asyncio.TimeoutError:
                    await ctx.channel.send('timed out, canceling process')
                    return await msg.delete()
                else:    
                    if str(reaction.emoji) == '👍':
                        await ctx.channel.send('processing audio, may take a while depending on size of playlist (be aware some items in playlist may not be avaliable)')
                        YDL_OPTIONS = {
                            'default_search': 'auto',
                            'format' :'--yes-playlist, bestaudio',
                            'forceduration': True,
                        }
                        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                            info = ydl.extract_info(url, download=False)
                            name = info['title']
                            for key in info['entries']:
                                title = key['title']
                                if server.id not in self.queue_name:
                                    self.queue_name[server.id] = [title]
                                else: 
                                    self.queue_name[server.id].append(title)
                                url2 = key['formats'][0]['url']
                                if server.id not in self.queue:
                                    self.queue[server.id] = [url2]
                                else:
                                    self.queue[server.id].append(url2)  
                                
                            source = await discord.FFmpegOpusAudio.from_probe(info['entries'][0]['formats'][0]['url'], **FFMPEG_OPTIONS)
                            try:
                                await ctx.channel.send(f'queued playlist: **{name}**')
                                vc.play(source, after=lambda e:asyncio.run(check_queue(self, ctx, server.id)))
                            except ClientException:
                                pass    
                    elif str(reaction.emoji) == '👎':
                        vc = ctx.voice_client
                        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                            info = ydl.extract_info(url, download=False)
                            title = info.get('title', None)
                            if server.id not in self.queue:
                                self.queue[server.id] = [url]
                            else:
                                self.queue[server.id].append(url)
                            if server.id not in self.queue_name:
                                self.queue_name[server.id] = [title]
                            else: 
                                self.queue_name[server.id].append(title)
                            url2 = info['formats'][0]['url']
                            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                            try:
                                await ctx.channel.send(f'queued **{title}**')
                                vc.play(source, after=lambda e:asyncio.run(check_queue(self, ctx, server.id)))
                            except ClientException:
                                pass  
            else:
                vc = ctx.voice_client
                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', None)
                    if server.id not in self.queue:
                        self.queue[server.id] = [url]
                    else:
                        self.queue[server.id].append(url)
                    if server.id not in self.queue_name:
                        self.queue_name[server.id] = [title]
                    else: 
                        self.queue_name[server.id].append(title)
                    url2 = info['formats'][0]['url']
                    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                    try:
                        await ctx.channel.send(f'queued **{title}**')
                        vc.play(source, after=lambda e:asyncio.run(check_queue(self, ctx, server.id)))
                    except ClientException:
                        pass  

        else:
            print('not valid url, using keyword')
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['entries'][0]['url']
                title = info['entries'][0]['title']
                if server.id not in self.queue_name:
                    self.queue_name[server.id] = [title]
                else: 
                    self.queue_name[server.id].append(title)
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                try:
                    await ctx.channel.send(f'queued **{title}**')
                    vc.play(source, after=lambda e:asyncio.run(check_queue(self, ctx, server.id)))
                except ClientException:
                    pass  
    
    @commands.command()
    async def pause(self, ctx, member: discord.Member):
        try:
            await member.edit(mute=True)
        except:
            await ctx.channel.send('user is not connected to voice/is paused already')
        
    @commands.command()
    async def unpause(self, ctx, member: discord.Member):
        try:
            await member.edit(mute=False)
        except:
            await ctx.channel.send('user is not connected to voice/is not paused')
            
    @commands.command()
    async def shuffle(self, ctx, member: discord.Member):
        voice_channel = ctx.guild.voice_channels
        await member.move_to(voice_channel[1])
        time.sleep(1)
        await member.move_to(voice_channel[0])
        time.sleep(1)
        await member.move_to(voice_channel[1])
        time.sleep(1)
        await member.move_to(voice_channel[0])
        time.sleep(1)
        await member.move_to(voice_channel[1])
        time.sleep(1)
        await member.move_to(voice_channel[0])
    
    @commands.command()
    async def skip(self, ctx):
        server = ctx.message.guild
        vc = ctx.voice_client
        vc.stop()
        await check_queue(self, ctx, server.id)
    
    @commands.command(name='q', aliases=['queue'])
    async def q(self, ctx):
        server = ctx.message.guild
        await ctx.channel.send('Currently Queued:\n')
        try:
            await ctx.channel.send('\n'.join(self.queue_name[server.id]))
        except:
            await ctx.channel.send('None')

async def check_queue(self, ctx, idy):
    try:
        self.queue[idy].pop(0)
        self.queue_name[idy].pop(0)
    except:
        pass
    try:                
        if self.queue[idy] != []:
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
                info = ydl.extract_info(self.queue[idy][0], download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                try:
                    vc.play(source, after=lambda e:asyncio.run(check_queue(self, ctx, idy)))
                except ClientException:
                    pass 
    except:
        await ctx.channel.send('nothing in queue')
        
def setup(client):
    client.add_cog(music(client))