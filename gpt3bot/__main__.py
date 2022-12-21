import os
from pathlib import Path
from abc import ABC
from discord.ext import bridge

import discord
import aioredis
import json

__name__ = "GPT3Bot"
__version__ = "0.0.1"
__author__ = "woo200"

data_dir = "/app/data"
dir_name = "/app/gpt3bot"

enabled_ext = [
    "gpt3bot.cogs.settings",
    "gpt3bot.cogs.gptchat",
]

# this is a pretty dumb way of doing things, but it works
intents = discord.Intents.all()

# check if the init_settings.json file exists and if not, create it
if not Path(os.path.join(data_dir, "init_settings.json")).exists():
    print("No init_settings.json file found. Creating one now.")
    settings_dict_empty = {
        "discord_token": "",
        "openai_key": "",
        "prefix": "!"
    }
    # write the dict as json to the init_settings.json file with the json library
    with open(os.path.join(data_dir, "init_settings.json"), "w") as f:
        # dump the dict as json to the file with an indent of 4 and support for utf-8
        json.dump(settings_dict_empty, f, indent=4, ensure_ascii=False)
    # make the user 1000 the owner of the file, so they can edit it
    os.chown(os.path.join(data_dir, "init_settings.json"), 1000, 1000)

    # exit the program
    exit(1)

# load the init_settings.json file with the json library
with open(os.path.join(data_dir, "init_settings.json"), "r") as f:
    try:
        settings_dict = json.load(f)
        discord_token = settings_dict["discord_token"]
        openai_key = settings_dict["openai_key"]
        command_prefix = settings_dict["prefix"]

    except json.decoder.JSONDecodeError:
        print("init_settings.json is not valid json. Please fix it.")
        exit(1)


class GPT3Bot(bridge.Bot, ABC):
    def __init__(self, command_prefix, **kwargs):
        super().__init__(command_prefix, **kwargs)

        self.openai_key = openai_key
        self.data_dir = data_dir
        
        print("Connecting to redis...")
        try:
            self.redis = aioredis.Redis(host="redis", db=1, decode_responses=True)
            self.redis_repost = aioredis.Redis(host="redis", db=2, decode_responses=True)
            self.redis_welcomes = aioredis.Redis(host="redis", db=3, decode_responses=True)
            print("Connection successful.")
        except aioredis.ConnectionError:
            print("Redis connection failed. Check if redis is running.")
            exit(1)

    async def on_ready(self):
        print("Bot Started.")


# create the bot instance
print(f"Starting GPT3Bot v{__version__} ...")
bot = GPT3Bot(command_prefix, intents=intents)
print(f"Loading {len(enabled_ext)} extension(s): \n")

# load the cogs aka extensions
for ext in enabled_ext:
    try:
        print(f"   loading {ext}")
        bot.load_extension(ext)
    except Exception as exc:
        print(f"error loading {ext}")
        raise exc

try:
    bot.run(discord_token)
except discord.LoginFailure:
    print("Login failed. Check your token. If you don't have a token, get one from https://discordapp.com/developers/applications/me")
    exit(1)