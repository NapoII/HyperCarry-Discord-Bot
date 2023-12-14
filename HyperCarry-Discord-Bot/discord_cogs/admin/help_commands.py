"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This COG is for embed a help information for Rust.
exampel : cctv codes

https://embed.dan.onl/
------------------------------------------------
"""
# 
from discord.ext import commands, tasks
from discord.ext import commands
from util.__funktion__ import *
import random
import discord
from discord import app_commands
from discord import app_commands, ui
from discord import Color
import asyncio
from datetime import datetime

# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)

token_config_dir = os.path.normpath(os.path.join(bot_folder, "cfg", "token.ini"))

# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")

steam_token = read_config(token_config_dir, "steam", "steam_token")
json_path_server_channel_data = os.path.join(current_dir, "server_channel_data.json")

bot_cmd_channel = read_config(config_dir, "channel", "bot_cmd_channel_id")


guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1



class help_commands(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("\n --> server_system_setup\n")

    @commands.command()
    async def help(self, ctx):
        
        embed = discord.Embed(title="!help",
                      description="""
                      ****Voice channel commands:****

                      > To create your own voice channel go to the channel:
                      > <#{create_voice_c_id}>
                      
                      > `/vc_help`
                      > Shows you a list of all commands and your channels on which you are an administrator (will be posted in your VC text channel).
                      
                      > `/vc_stay`
                      > Switch the status whether the server may be deleted after leaving
                      
                      > `/vc_rename`
                      > Rename the Voice Channel.
                      
                      > `vc_limit`
                      > Set the maximum number of users.

                      > `/vc_kick`
                      > Kick a User from your Channel

                      > `/vc_ban`
                      >Ban a User from your Channel
                      """,
                      colour=0x00b0f4)
        await ctx.send(embed=embed)




async def setup(bot: commands.Bot):
    await bot.add_cog(help_commands(bot), guild=discord.Object(guild_id))