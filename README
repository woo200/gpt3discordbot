# GPT3 Discord Bot

## Installation
This bot requires Docker to run, You may find instructions on installing docker for your native operating system [Here](https://docs.docker.com/get-docker/).

### Clone the repository
```bash
git clone https://github.com/woo200/gpt3discordbot
```

### Go to folder and start the docker container
```bash
cd gpt3discordbot
sudo docker-compose up
```
Docker will install all the neccesary dependencies, which may take a while. Once it is finished, hit ctrl C to stop it.

### Set API keys
Open `data/init_settings.json` to find something like this:
```json
{
    "discord_token": "",
    "openai_key": "",
    "prefix": "!"
}
```
Populate this with your discord bots token & openai key.

## Using the bot

### Setting a channel 
Use the `/toggle_gpt3` command in a channel to toggle the bot on and off in that channel. Administrators have this permission by default

### Setting moderator roles
To allow non-administrator users to use this bots features, you may use the `/add_mod [role]` command, which will give permission to use this bots commands to anyone with `[role]` 