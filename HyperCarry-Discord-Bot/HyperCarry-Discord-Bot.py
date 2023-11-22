"""Full Doku on: https://github.com/NapoII/HyperCarry-Disocrd-Bot"
-----------------------------------------------
Discord Community Bot with the feat:
            - Support Ticket System
            - Auto Voice channel System
            - User Pic his role System

To do: add_new_game for role pick command
https://discord.com/developers
https://embed.dan.onl/
------------------------------------------------
"""

#### import

import os
import sys

import discord
from discord.ext import commands, tasks
from platform import python_version


from util.__funktion__ import *


#### pre Var
v = "0.0.1 - Hello World"
py_name = os.path.basename(__file__)

file_path = os.path.normpath(os.path.dirname(sys.argv[0]))
config_dir = file_path + os.path.sep + "cfg"+ os.path.sep +"config.ini"

################################################################################################################################
# Load Config
token_config_dir = os.path.normpath(os.path.join(file_path, "cfg", "token.ini"))

# Client
while True:
    try:
        Discord_token = read_config(token_config_dir, "discord", "token")
        Application_ID = read_config(token_config_dir, "discord", "application_id")

        guild_id = read_config(config_dir, "client", "guild_id", "int")
        guild = discord.Object(id=guild_id)
        praefix = read_config(config_dir, "client", "praefix")
        activity_text = (read_config(config_dir, "client", "activity"))
        activity = Discord_Activity(activity_text)

        break
    except:
        print(f"Fill in the empty fields in both config files! \n token_config -> [{token_config_dir}]\nconfig_dir -> [{config_dir}]")

# channel
bot_cmd_channel_id = read_config(config_dir, "channel", "bot_cmd_channel_id", "int")
delt_msg_channel_id = read_config(config_dir, "channel", "delt_msg_channel_id", "int")


################################################################################################################################

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=praefix,
            intents=discord.Intents.all(),
            application_id=Application_ID,
            activity=activity
        )
        self.initial_extensions = [
            "discord_cogs.admin.pre_setup",
            "discord_cogs.ticket_system.ticket_system",
            "discord_cogs.channel_hopper.channel_hopper",
            "discord_cogs.pick_a_role.pick_a_role",
            "discord_cogs.game_server.discord_gameserver_struk"
        ]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild=discord.Object(guild_id))


    async def on_ready(self):
        guild = self.get_guild(guild_id)  # Access guild from the class attribute
        text = f"\n\nThe Bot: [ {self.user} | ID:{self.user.id} ] is connected to [{guild.name}] id: [{guild.id}]\nActivity_text:[{activity_text}]\n\n📶 Bot is Online and Rdy to Run... 📶 \n"
        print(str(text))
        print('------')

        print(f'Logged in as {self.user} (ID: {self.user.id})')

        # Retrieve bot_cmd_channel_id without type conversion
        bot_cmd_channel_id = read_config(config_dir, "channel", "bot_cmd_channel_id", "int")

        # Check if bot_cmd_channel_id is valid
        if bot_cmd_channel_id is not None:
            bot_cmd_channel = guild.get_channel(bot_cmd_channel_id)

            # Check if bot_cmd_channel is a valid TextChannel
            if bot_cmd_channel is not None and isinstance(bot_cmd_channel, discord.TextChannel):
                text = f"\n\nThe Bot: [ {self.user} | ID:{self.user.id} ] is connected to [{guild.name}] id: [{guild.id}]\nActivity_text:[{activity_text}]\n\n📶 Bot is Online and Rdy to Run... 📶 \n"
                print(str(text))

                embed = discord.Embed(title=py_name, color=0xff80ff)
                embed.set_author(name="created by Napo_II", url="https://github.com/NapoII/HyperCarry-Disocrd-Bot")
                embed.set_thumbnail(url="https://i.imgur.com/hcVwvZF.png")
                embed.add_field(name="Version", value=v, inline=True)
                embed.add_field(name="python", value=f"{python_version()}", inline=True)
                embed.add_field(name="github", value="https://github.com/NapoII/HyperCarry-Discord-Bot", inline=False)
                await bot_cmd_channel.send(embed=embed)

                dc_time = discord_time_convert(time.time())
                embed = discord.Embed(title="📶 Bot is Online and Rdy to Run... 📶",  description=f"{dc_time}", color=0xff8080)
                embed.add_field(name="client.name", value=self.user.name, inline=True)
                embed.add_field(name="guild.name", value=guild.name, inline=True)
                embed.add_field(name="guild.id", value=str(guild.id), inline=True)
                await bot_cmd_channel.send(embed=embed)

bot = MyBot()
bot.run(Discord_token)