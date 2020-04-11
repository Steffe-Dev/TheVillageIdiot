import os
import discord
from dotenv import load_dotenv

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


@bot.command(name='h')
async def help_list(ctx):
    response = (
        'Hi there! I\'m an experimental bot written by the admin of this server, STeFFe, and my capabilities are rather limited - hence the name.\n\n'
        'Here follows a list of ther commands currently supported:\n'
        '>>h:    Displays this list\n'
        '\n'
        'My creator hopes to improve my functionality in the future.'
    )
    await ctx.send(response)

@bot.command(name='join', help='Joins the bot testing voice channel')
async def join_test(ctx):
    channel = bot.get_channel(int(BOT_VOICE_CH))
    await channel.connect()

@bot.command(name='leave', help='Leaves the bot testing voice channel')
async def leave_test(ctx):
    await ctx.voice_client.disconnect() 

bot.run(TOKEN)
















#################################### NOTES ##############################################################################
# # defines subclass for implementing an event handler
# class CustomClient(discord.Client):
#     async def on_ready(self):
#         print(f'{self.user} has connected to Discord!')

# client = CustomClient()
# client.run(TOKEN)