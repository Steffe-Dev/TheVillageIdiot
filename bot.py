import os
import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SYS_MSSG = os.getenv('DISCORD_SYS_MSSG')
# initializes client
bot = commands.Bot(command_prefix='>>')

# defines event handler for when client connects to discord
@client.event
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
@client.event
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
    bot.run(TOKEN)
















#################################### NOTES ##############################################################################
# # defines subclass for implementing an event handler
# class CustomClient(discord.Client):
#     async def on_ready(self):
#         print(f'{self.user} has connected to Discord!')

# client = CustomClient()
# client.run(TOKEN)