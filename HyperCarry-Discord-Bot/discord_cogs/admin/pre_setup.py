"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This COG is for embed a help information for Rust.
exampel : cctv codes


------------------------------------------------
"""
# 
from discord.ext import commands, tasks
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



class server_system_setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir  # Beispiel-Konfigurationsverzeichnis


        # Hier wird die Methode beim Start des Bots aufgerufen
        self.bot.loop.create_task(self.setup_ticket_system())

    async def setup_ticket_system(self):
        print ("\n --> server_system_setup\n")
        await self.bot.wait_until_ready()  
        guild = self.bot.get_guild(guild_id)

        was_created_list = []


# Creates a new Role
        role_name = "🤖-Bot-Admin"
        role_colour = discord.Color.from_rgb(255,255,255)
        bot_admin_role_id = read_config(config_dir,"role", "bot_admin_role_id", "int")
        bot_admin_role = discord.utils.get(guild.roles, id=bot_admin_role_id)

        if bot_admin_role != None:
            print(f"The role {bot_admin_role.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            bot_admin_role = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {bot_admin_role.name} was created.")
            write_config(config_dir, "role", "bot_admin_role_id", bot_admin_role.id)


# Creates a new category
        category_name = "--------💻 - Admin - 💻--------"
        category_adminl_id = read_config(config_dir,"channel", "open_a_ticket_channel_id", "int")
        category_admin = discord.utils.get(guild.text_channels, id=category_adminl_id)

        if category_admin != None:
            print(f"The category {category_admin.name} already exists.")

        else:
            print(f"The category {category_name} does not yet exist and will now be created")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, view_channel=False),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }

            category_admin = await guild.create_category(category_name, overwrites=overwrites)

            bot_admin_role_id = read_config(config_dir,"role", "bot_admin_role_id", "int")
            bot_admin_role = discord.utils.get(guild.roles, id = bot_admin_role_id)
            await category_admin.set_permissions(bot_admin_role, read_messages=True, send_messages=True)

            print(f"The category {category_name} was created.")
            category_admin_name = category_admin.name
            category_admin_id = category_admin.id
            write_config(config_dir, "category","category_admin_id", category_admin_id)
            
            was_created_list.append(category_admin)


# Creates a new text channel
        bot_cmd_channel_name = "💻-bot-cmd"
        bot_cmd_channel_id = read_config(config_dir,"channel", "bot_cmd_channel_id", "int")
        bot_cmd_channel = discord.utils.get(guild.text_channels, id=bot_cmd_channel_id)

        if bot_cmd_channel != None:
            print(f"The channel {bot_cmd_channel.name} already exists.")
        else:
            print(f"The channel {bot_cmd_channel_name} does not exist.")

            category_admin_id = read_config(config_dir, "category", "category_admin_id", "int")
            category_admin = discord.utils.get(guild.categories, id=category_admin_id)


            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, view_channel=False),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }


            bot_cmd_channel = await guild.create_text_channel(bot_cmd_channel_name, category=category_admin, overwrites=overwrites)
            await bot_cmd_channel.set_permissions(guild.default_role, read_messages=False)

            bot_admin_role_id = read_config(config_dir,"role", "bot_admin_role_id", "int")
            bot_admin_role = discord.utils.get(guild.roles, id = bot_admin_role_id)
            await bot_cmd_channel.set_permissions(bot_admin_role, read_messages=True, send_messages=True)
            
            print(f"The channel {bot_cmd_channel.name} was created.")
            write_config(config_dir, "channel", "bot_cmd_channel_id", bot_cmd_channel.id)

            was_created_list.append(bot_cmd_channel)

            embed = discord.Embed(title="Attention!", color=0x8080ff)
            embed.set_author(name=f"@{guild.name}",
                            icon_url=f"https://i.imgur.com/OfrhTsM.png")
            embed.set_thumbnail(url="https://i.imgur.com/s5ZWwpZ.png")
            embed_text = f"🔒 Please make sure to adjust the role settings for\n<#{category_admin_id}>\nto restrict channel visibility to authorized users, instead of allowing it to be visible to everyone. 🔓"
            embed.add_field(name="Attention!",value=embed_text, inline=True)
            await bot_cmd_channel.send(embed=embed)

            gif_url = r"https://i.imgur.com/F1DWMfO.gif"

            text = ""
            list_of_hiden_commands = ["/add_server", "/delt_server"]
            for hide_command in list_of_hiden_commands:
                text = text + f" - `{hide_command}`\n"

            description=f"```Server settings > Intergation > Bot > Set commands ```\nThat only the Users with the Role <@&{bot_admin_role.id}>\ncan see/use the commands:\n\n{text}"


            embed = discord.Embed(title="/Commands Set rights manually",
                      description=description,
                      colour=0xff0000)

            embed.set_image(url=f"{gif_url}")
            await bot_cmd_channel.send(embed=embed)


        was_created_list_len = len(was_created_list)
        if was_created_list_len != 0:
            x = -1
            text = ""
            while True:
                x = x + 1
                if x == was_created_list_len:
                    break
                id = was_created_list[x].id
                text = text + f"<#{id}>\n"

            dc_time = discord_time_convert(time.time())
            embed = discord.Embed(title=f"The following Main System Channels have been created:",
                                description=f"> The following channels had to be created:\n{text}\ncreated: {dc_time}",
                                colour=0xffff80)
            await bot_cmd_channel.send(embed=embed)



async def setup(bot: commands.Bot):
    await bot.add_cog(server_system_setup(bot), guild=discord.Object(guild_id))