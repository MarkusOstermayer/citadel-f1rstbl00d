import os
import requests
from discord.ext import tasks, commands
import discord
from discord import Embed
from dotenv import load_dotenv
import logging

# Load vars and default values
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
logging.basicConfig(level=logging.INFO)
channel = None
usedblood = []


@bot.event
async def on_ready():
    """
    This is the code which will be executed after the bot is ready to be used.

    Inside here the bot will connect to the channel and start the background task.
    """
    await bot.change_presence(
        status=discord.Status.idle, activity=discord.Game(name="FBB - First Blood Bot")
    )
    global channel
    try:
        channel = bot.get_channel(int(CHANNEL_ID))
        if channel is None:
            print(f"Channel with ID {CHANNEL_ID} not found")
        else:
            logging.info(f"Connected to channel {channel.name}")
    except Exception as e:
        print(f"Error when connecting to channel: {e}")
    print(f"{bot.user} is connected now!:\n")
    my_background_task.start()


@bot.command()
async def firstblood(ctx):
    """
    This is the command which will be executed when the user types $firstblood in the chat.

    It will send a message with the explanation of what FirstBloods are.
    """
    print("Command FIRSTBLOOD called")
    await ctx.send(
        "# HTL TOPHACK FIRST BLOODS :bird:\n"
        "## What are first bloods?\n"
        "In Capture the Flag (CTF) competitions, **first bloods** refer to the initial successful capture of a flag by a team.\n"
        "It signifies the first team to penetrate the opponent's defenses and secure a flag, often earning points or recognition for their accomplishment.\n"
        "First bloods set the tone for the competition, highlighting the agility and strategic prowess of the team that achieves them.\n"
        "## So why are first bloods important now?\n"
        "It's simple: **First bloods** show the other teams that you are build different.\n"
        "You are simply better than others. :shushing_face: :deaf_person: \n"
    )


@tasks.loop(seconds=10)
async def my_background_task():
    """
    This is the background task which will be executed every 10 seconds.

    It will check for new FirstBloods and send a message to the channel if there are any.
    """
    data = get_all_firstblood()
    if data is not None:
        global usedblood
        if data != []:
            for item in data:
                if item not in usedblood:
                    embed = Embed(
                        title=f"Challenge: {item['challenge_name']}", color=0xFF0000
                    )
                    embed.set_author(name="CHALLENGE SOLVED (FIRST BLOOD)")
                    embed.description = f"- Solved by: **@{item['username']}**\n- Time solved: **{item['date'].split('T')[1]}**\n- Category: {item['challenge_category']}\n- Difficulty: {item['challenge_difficulty']}\n\n Good job!"
                    embed.set_thumbnail(
                        url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimg00.deviantart.net%2Fb604%2Fi%2F2012%2F228%2F7%2F5%2Fblood_drop_man_by_unicorn_skydancer08-d5bazt3.png&f=1&nofb=1&ipt=3f0c3f8c5835c0ce8ddcfb70832b1c40ff59054b23266a6f5cbc3977e13d9fc4&ipo=images"
                    )  # Replace with your image URL (Current one is a banger)
                    new_msg = await channel.send(embed=embed)
                    await new_msg.add_reaction("🩸")
                    usedblood.append(item)
    else:
        logging.error("The request failed")


def get_all_firstblood():
    """
    This function will make a request to the FastAPI server to get all FirstBloods.

    If the request is successful, it will return the data. Otherwise, it will return None.
    """
    url = "http://webdc:80/firstbloods/all/?update_was_sent=true"
    headers = {"Authorization": f"Bearer {os.getenv('BLOODTOKEN')}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


bot.run(TOKEN)
