# Discord Bot for The Village
#
# Known Issues:
#   if roll is called without a param, no msg is displayed to correct the user.
#   First line in meme caches is corrupt

import os
import discord
import random
import asyncio
from discord import opus
from dotenv import load_dotenv

import urllib, io
import re


from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SYS_MSSG = os.getenv('DISCORD_SYS_MSSG')
BOT_VOICE_CH = os.getenv('DISCORD_BOT_VOICE_CH')
# initializes client
bot = commands.Bot(command_prefix='>>')

# defines event handler for when client connects to discord
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="meme cache"))
    await meme_cache()
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    
    print(
        f'{bot.user} has connected to the following Discord guild:\n'
        f'{guild.name}(id: {guild.id})'    
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    await bot.change_presence(activity=discord.Game(name=">>help"))

# when new member joins the server
@bot.event
async def on_member_join(member):
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    # send message to the system messages channel
    for channel in guild.channels:
        if channel.name == 'Admin':
            for channel2 in channel.channels:
                if channel2.id == int(SYS_MSSG):
                    break

    await channel2.send(
        f'Hi {member.name}, welcome to {guild.name}!'
    )
    role = discord.utils.get(member.guild.roles, name="Member")
    await member.add_roles(role)

# Webhook stuff
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content.startswith(">>"):
        return

    channel = find_channel('meme-theater')
    #standard meme format    
    urls = re.findall("https://i.redd.it/.{13}[.]{1}[jpngif]{3}", message.content)

    #check if r/unexpected
    if len(urls) == 0:
        urls = re.findall("https://v.redd.it/.{13}", message.content)

    #another r/unexpected format
    if len(urls) == 0:
        urls = re.findall("https://i.imgur.com/.{13}[.]{1}[jpngif]{3}", message.content)
    
    if len(urls) == 0:
        urls = re.findall("https://i.*[.]{1}[jpngif]{3}", message.content)

    if message.channel.name == "memes-raw":
        if len(urls) > 0:
            await channel.send(urls[0])
        else:
            await channel.send("No match")


@bot.command(name='wipe_channel', help='wipes all messages on a channel containing a substring')
async def wipe(ctx, channel, contains):
    cnl = find_channel(channel)
    async for message in cnl.history(limit=1000000000):
        if message.content.find(contains) != -1:
            await discord.Message.delete(message)

@bot.command(name='resend', help='resends messages on a channel, {cnl} {amount}')
async def resend(ctx, channel, amount):
    cnl = find_channel(channel)
    async for message in cnl.history(limit=int(amount)):
        msg = message.content
        if msg.startswith('>>'):
            continue
        await discord.Message.delete(message)
        await cnl.send(msg)

@bot.command(name='meme_normal', help='sends a random meme from the meme theater')
async def mn(ctx):
    await meme(ctx,'1')


@bot.command(name='meme_quality', help='sends a random meme from the hall of fame')
async def mq(ctx):
    await meme(ctx,'quality')

async def meme(ctx, quality):
    li = [
        "Please wait while I fetch you a quality meme from our collection...\n",
        "Your meme shall be  summoned shortly...\n",
        "Loading dank meme...\n",
        "Allow me a few moments to procure your meme...\n",
        "To meme, or not to meme...\n",
        "Scanning meme database...\n",
        "Loading meme cannon...\n",
        "The suspense created while waiting for a meme is scientifically proven to increase its effective funniness...\n",
        "Every sixty seconds in Africa, one minute passes...\n",
        "Wait for it, wait for it...\n",
        "Any second now...\n"
    ]

    msg_num = random.randint(0,len(li)-1)
    await ctx.channel.send(li[msg_num])

    if quality == 'quality':
        channel = find_channel('hall-of-fame')
        fil = open(f"./memes/hof.txt", 'r')
    else:
        channel = find_channel('meme-theater')
        fil = open(f"./memes/memes.txt", 'r')

    max = int(fil.readline())
    i = 0
    num = random.randint(0,max)
    for line in fil:
        i += 1
        print(f'{i}\'th msg, and it is: {line}. Num is {num}')
        if (i == num):
            break

    print(f'Number of memes in database: {max}')
    await ctx.channel.send(line)
    await ctx.channel.send(f'Number of memes in database: {max}')

@bot.command(name='meme_cache', help='Forces a manual update to the txt file holding a cache of all the messages in the meme theater.')
async def cache(ctx):
    await meme_cache()

async def meme_cache():
    print("Running meme cache...")
    await meme_cache_lower("meme-theater", "./memes/memes.txt")
    await meme_cache_lower("hall-of-fame", "./memes/hof.txt")
    print("Successfully ran meme_cache.")

async def meme_cache_lower(channel, output):
    file_name_mt = open(output, 'r+')
    channel = find_channel(channel)
    i = 0
    async for msg in channel.history(limit=1000000):
        if msg.content.startswith('https://i.redd.it'):
            i += 1
            file_name_mt.write(msg.content + '\n')
    content = file_name_mt.read()
    file_name_mt.seek(0,0)
    file_name_mt.write(str(i) + '\n' + content)

@bot.command(name='note', help='Makes a note that can be recalled. \nUsage: >>note *name* *content*')
async def note(ctx, name, note):
    file_name = open(f"./{name}.txt", 'a')
    file_name.write(note)
    await ctx.channel.send("Successfully wrote to file")
        

@bot.command(name='open_text_file', help='Opens a text file \n(They are saved on my pc, and then on a public github, so no sensitive info)')
async def open_text(ctx, name):
    try:
        file_name = open(f"./{name}.txt", 'r')
        await ctx.channel.send(f"Opening file: {name}.txt")
        for line in file_name:
            await ctx.channel.send(line)
    except:
        await ctx.channel.send("Could not locate a file with that name!")

@bot.command(name='delete_text_file', help='Deletes a text file \n(They are saved on my pc, and then on a public github)')
@commands.has_role('Chiefz')
async def delete_text(ctx, name):
    if os.path.exists(f"./{name}.txt"):
        await ctx.channel.send(f"Deleting file: {name}.txt")
        os.remove(f"./{name}.txt")
    else:
        await ctx.channel.send("Could not locate a file with that name!")

@bot.command(name='list_files', help='List all created text files \n(They are saved on my pc, and then on a public github)')
async def list_text(ctx):
    path = './'

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.txt' in file:
                files.append(file)
    for f in files:
        await ctx.channel.send(f)

@bot.command(name='hi', help='Prints a greeting')
async def help_list(ctx):
    response = (
        'Hi there! I\'m an experimental bot written by the admin of this server, STeFFe, and my capabilities are rather limited - hence the name.\n\n'
        'I can apparently post memes, though. xD\n'
        'My creator hopes to improve my functionality in the future.'
        'Use the >>help command for a list of what I can do.'
    )
    await ctx.send(response)

@bot.command(name='join', help='Joins the current channel')
async def join_test(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='Leaves the current channel', catagory='commands')
async def leave_test(ctx):
    await ctx.voice_client.disconnect() 

@bot.command(name='roll', help='Rolls a random number between 0 and the specified max(inclusive)')
async def roll(ctx, max: int):
    num = random.randint(0,max)
    fin = str(num)
    await ctx.send(f'{ctx.author.name} rolled {fin}')

@bot.command(name='create_channel', help='Creates a new channel in current category, with params <channel_name> <is_voice> (Use True/False)')
@commands.has_role('Chiefz')
async def create_channel(ctx, name, is_voice: bool):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels,name=name)
    if not existing_channel:
        if is_voice:
            print(f'Creating a new voice channel with name: {name}.')
            await ctx.channel.send(f'Creating a new voice channel with name: {name}.')
            await guild.create_voice_channel(name, category=ctx.channel.category)
        else:
            print(f'Creating a new text channel with name: {name}.')
            await ctx.channel.send(f'Creating a new text channel with name: {name}.')
            await guild.create_text_channel(name, category=ctx.channel.category)

@bot.command(name='play', help='Plays from an audio source (Not Functional)')
async def plays(ctx, source):
    vc = bot.voice_clients[0]
    audio_src = discord.PCMAudio('C:\\Users\\Francois\\Music\\Downloaded by MediaHuman\\The Black Keys - Little Black Submarines.mp3')
    await vc.play(audio_src)

#functions
def find_channel(cnl):
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    for channel in guild.channels:
        if channel.name == cnl:
            return channel






bot.run(TOKEN)
















#################################### NOTES ##############################################################################
# # defines subclass for implementing an event handler
# class CustomClient(discord.Client):
#     async def on_ready(self):
#         print(f'{self.user} has connected to Discord!')

# client = CustomClient()
# client.run(TOKEN)
