import aioredis
import discord

from discord.ext import commands

def preprocessor(a):
    if type(a) is str:
        return a.upper()
    else:
        return a


async def can_change_settings(ctx: commands.Context):
    """
    Checks if the user has the permission to change settings. (Owner and admin)
    """
    channel: discord.TextChannel = ctx.channel
    is_owner = await ctx.bot.is_owner(ctx.author)
    is_admin = channel.permissions_for(ctx.author).administrator
    return is_owner or is_admin


async def mods_can_change_settings(ctx: commands.Context):
    """
    Checks if the user has the permission to change settings. (Mods included)
    """
    key = f"mod_roles:{ctx.guild.id}"
    channel: discord.TextChannel = ctx.channel
    is_owner = await ctx.bot.is_owner(ctx.author)
    is_admin = channel.permissions_for(ctx.author).administrator
    redis: aioredis.Redis = ctx.bot.redis
    is_mod = False
    if ctx.bot.redis:
        pipe = redis.pipeline()
        for role in ctx.author.roles:
            await pipe.sismember(key, role.id)
        is_mod = any(await pipe.execute())
        await pipe.close()
    return is_owner or is_admin or is_mod


class SettingsCog(commands.Cog, name="settings"):
    """
    Settings Cog. Allows the bot owner or admins to change settings for their server. All settings are stored in Redis
    and only apply to the server the command was used in. Global settings are not a thing (yet).
    """
    def __init__(self, bot):
        self.bot: discord.Client = bot
        self.redis: aioredis.Redis = self.bot.redis

    @discord.command(name="add_mod", description="Add a moderator role. Mod commands will be available to this role.")
    async def _add_mod(self, ctx: commands.Context, role: discord.Role):
        """
        Allows mod perms to add a moderator role. Anyone with this role will be able to access mod features of KiteBot. 
        """
        if not ctx.channel.permissions_for(ctx.author).administrator:
            await ctx.respond("You do not have permission to do this.")
            return
        
        key = f"mod_roles:{ctx.guild.id}"   # I wanted to call them snowflakes :troll: but that would result in bad readability
        if not await self.redis.sismember(key, role.id):
            await self.redis.sadd(key, role.id)
            await ctx.respond(f"{role.name} is now a moderator role")
        else:
            try:
                await self.redis.srem(key, role.id)
            except aioredis.ResponseError:
                await ctx.respond(f"{role.name} is not a moderator role")
                return
            await ctx.respond(f"{role.name} is no longer a moderator role")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # this initializes the settings for the guild the bot joins
        init_dict = {}
        # check if there already are settings for the guild present
        if not await self.redis.hexists(guild.id, "IMAGE"):
            # set the settings that were defined in init_dict
            await self.redis.hmset(guild.id, init_dict)


def setup(bot):
    bot.add_cog(SettingsCog(bot))