import discord
import aioredis
import gpt3bot
from urllib.parse import urlparse, parse_qs, urlencode
from discord.ext import commands, bridge

from gpt3bot.cogs.settings import mods_can_change_settings

# Automatically removed tracking content from links and de-ampifies links when the setting is turned on
class GptChatCog(commands.Cog, name="GPT3 Chat"):
    def __init__(self, bot):
        self.bot: gpt3bot.GPT3Bot = bot
        self.redis: aioredis.Redis = bot.redis

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Check if the user is a bot 
        if message.author.bot:
            return
        
        # Check if the bot is enabled
        if not await self.redis.sismember(f"gpt3bot_channels:{message.guild.id}", message.channel.id):
            return
        
        message.channel.send("Test")

    @commands.check(mods_can_change_settings)
    @bridge.bridge_command(name="enable_gpt3",
                           description="Enable the GPT3 bot in a channel")
    async def add_uwu_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        if not await mods_can_change_settings(ctx):
            return await ctx.respond("You don't have permission to change settings.")
        
        key = f"gpt3bot_channels:{ctx.guild.id}"
        if not await self.redis.sismember(key, channel.id):
            await self.redis.sadd(key, channel.id)
            await ctx.respond(f"GPT3 bot has been enabled in {channel.mention}")
            print(f"{ctx.guild.name}:  {ctx.author.name}#{ctx.author.discriminator} GPT3BOT ENABLE #{channel.name}")
        else:
            try:
                await self.redis.srem(key, channel.id)
            except aioredis.ResponseError:
                await ctx.respond(f"GPT3 is not enabled in {channel.mention}")
                return

            await ctx.respond(f"GPT3 bot has been disabled in {channel.mention}")
            print(f"{ctx.guild.name}:  {ctx.author.name}#{ctx.author.discriminator} GPT3BOT DISABLE #{channel.name}")
    

def setup(bot):
    bot.add_cog(GptChatCog(bot))