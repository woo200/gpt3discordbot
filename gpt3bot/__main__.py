import os
from abc import ABC
from datetime import datetime
from pathlib import Path

import discord
import aioredis
import json

__name__ = "GPT3Bot"
__version__ = "0.0.1"
__author__ = "woo200"

data_dir = "/app/data"
dir_name = "/app/gpt3bot"

# Copied from thatredkite/gpt3bot

# this is a pretty dumb way of doing things, but it works
intents = discord.Intents.all()

# check if the init_settings.json file exists and if not, create it
if not Path(os.path.join(data_dir, "init_settings.json")).exists():
    print("No init_settings.json file found. Creating one now.")
    settings_dict_empty = {
        "discord_token": "",
        "openai_key": "",
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

    except json.decoder.JSONDecodeError:
        print("init_settings.json is not valid json. Please fix it.")
        exit(1)


class GPT3Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print("Ready!")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith("!hello"):
            await message.channel.send("Hello!")

# create the bot instance
print(f"Starting GPT3Bot v{__version__} ...")
bot = GPT3Bot(intents=intents)

try:
    bot.run(discord_token)
except discord.LoginFailure:
    print("Login failed. Check your token. If you don't have a token, get one from https://discordapp.com/developers/applications/me")
    exit(1)