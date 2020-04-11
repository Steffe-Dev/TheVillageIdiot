import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# initializes client
client = discord.Client()

# defines function for when client connects to discord
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)