# Discord Bot for The Village
#
# Known Issues:
#   if roll is called without a param, no msg is displayed to correct the user.

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
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    
    print(
        f'{bot.user} has connected to the following Discord guild:\n'
        f'{guild.name}(id: {guild.id})'    
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

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
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    for channel in guild.channels:
        if channel.name == 'meme-theater':
            break
    urls = re.findall("https://i.redd.it/.*[jpngif]{3}", message.content)
    
    if message.channel.name == "memes-raw":
        if len(urls) > 0:
            await channel.send(urls[0])
        else:
            await channel.send("No match")


@bot.command(name='wipe_channel', help='wipes all messages on a channel')
async def wipe(ctx, channel):
    for g in bot.guilds:
        if g.name == GUILD:
            break
    for cnl in g.channels:
        if cnl.name == channel:
            break
    print(f"deleting messages in {cnl}!",)
    async for message in cnl.history(limit=1000):
        await discord.Message.delete(message)



@bot.command(name='hi', help='Prints a greeting')
async def help_list(ctx):
    response = (
        'Hi there! I\'m an experimental bot written by the admin of this server, STeFFe, and my capabilities are rather limited - hence the name.\n\n'
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
@commands.has_role('Admin')
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
bot.run(TOKEN)
















#################################### NOTES ##############################################################################
# # defines subclass for implementing an event handler
# class CustomClient(discord.Client):
#     async def on_ready(self):
#         print(f'{self.user} has connected to Discord!')

# client = CustomClient()
# client.run(TOKEN)