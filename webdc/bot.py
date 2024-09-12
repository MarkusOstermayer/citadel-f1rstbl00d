import logging
import os
import tomllib

import discord
import requests
from discord import Embed
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv


# Load env vars
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

# Create the bot and set permissions and intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
logging.basicConfig(level=logging.INFO)
channel = None
usedblood = []

def load_config(filename: str="config.toml"):
    try:
        with open(filename, "rb") as f:
                data = tomllib.load(f)
    except tomllib.TOMLDecodeError as toml_error:
        logging.error(f"Format-Error in the toml-file: {toml_error}")
        exit(1)
    except FileNotFoundError as fnf_error:
        logging.error(f"{fnf_error}")
        exit(2)

    # Check that the keys needed for the bot are specified
    if "bot" not in data:
        logging.error("The config does not contain a [bot]-section!")
        exit(3)

    for needed_key in ["embed_thumbnail_url", "embed_thumbnail_url"]:
        if needed_key not in data["bot"]:
            logging.error(f"The [bot]-section does not contain a {needed_key}-value!")
            exit(4)

    return data

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
            logging.error(f"Channel with ID {CHANNEL_ID} not found")
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
    logging.info("Command FIRSTBLOOD called")
    await ctx.send(data["bot"]["firstblood_info_text"])


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
                        url=data["bot"]["embed_thumbnail_url"]
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

config = load_config(os.getenv('CONFIG_PATH', "./config.toml"))
bot.run(TOKEN)
