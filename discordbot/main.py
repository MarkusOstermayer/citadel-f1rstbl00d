# bot.py
import os
import requests
from discord.ext import tasks, commands
import discord
from discord import Embed
from dotenv import load_dotenv
import logging

# Load vars and default values
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
intents = discord.Intents.default()  
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
logging.basicConfig(level=logging.INFO)
channel = None
usedblood = []

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="FBB - First Blood Bot"))
    global channel
    try:
        channel = bot.get_channel(int(CHANNEL_ID))
        if channel is None:
            print(f'Channel with ID {CHANNEL_ID} not found')
        else:
            logging.info(f'Connected to channel {channel.name}')
    except Exception as e:
        print(f'Error when connecting to channel: {e}')
    print(
        f'{bot.user} is connected now!:\n'
    )
    my_background_task.start()  # Start the background task


@bot.command()
async def firstblood(ctx):
    print("Command FIRSTBLOOD called")
    # Generall explanation of bot
    await ctx.send("# HTL TOPHACK FIRST BLOODS :bird:\n"
                   "## What are first bloods?\n"
                   "In Capture the Flag (CTF) competitions, **first bloods** refer to the initial successful capture of a flag by a team.\n" 
                   "It signifies the first team to penetrate the opponent's defenses and secure a flag, often earning points or recognition for their accomplishment.\n" 
                   "First bloods set the tone for the competition, highlighting the agility and strategic prowess of the team that achieves them.\n"
                   "## So why are first bloods important now?\n"
                   "It's simple: **First bloods** show the other teams that you are build different.\n"
                   "You are simply better than others. :shushing_face: :deaf_person: \n"
                   )

@tasks.loop(seconds=10)  # Create a task that runs every 10 seconds
async def my_background_task():
    data = get_all_firstblood()
    if data is not None:
        global usedblood
        if data != []:
            for item in data:
                if item not in usedblood:
                    embed = Embed(title=f"Challenge ID: {item['challenge_id']}", color=0xff0000)
                    embed.set_author(name="CHALLENGE SOLVED (FIRST BLOOD)")
                    embed.description = f"- User ID: {item['user_id']}\n- Event ID: {item['event_id']}\n\n Good job!"
                    embed.set_thumbnail(url="https://media.discordapp.net/attachments/1223305032464597153/1223674823834603591/ppblood.png?ex=661ab6fc&is=660841fc&hm=57b1d3c85fdea033f5fd0c88ddd87d5ff248afefc655033835d700da60e6fa2e&=&format=webp&quality=lossless&width=332&height=350")  # Replace with your image URL
                    new_msg = await channel.send(embed=embed)
                    await new_msg.add_reaction("🩸")
                    usedblood.append(item)
    else:
        logging.error("The request failed")


def get_all_firstblood():
    url = "http://web:80/firstbloods/all/"
    headers = {
        "Authorization": f"Bearer {os.getenv('BLOODTOKEN')}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # If the request was successful, return the data
    else:
        return None  # If the request failed, return None


bot.run(TOKEN)