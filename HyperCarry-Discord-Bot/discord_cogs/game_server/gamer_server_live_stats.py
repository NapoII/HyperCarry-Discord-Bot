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


guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1



class server_stats_system_setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir 

        self.bot.loop.create_task(self.setup_ticket_system())

    async def setup_ticket_system(self):
        print ("\n --> server_stats_system_setup\n")
        await self.bot.wait_until_ready()  
        guild = self.bot.get_guild(guild_id)


        was_created_list = []

# Creates a new categoryX-servers
        category_name = "-------🌍- Servers - 🌍-------"
        category_servers_id = read_config(config_dir,"category", "category_servers_id", "int")
        category_servers = discord.utils.get(guild.categories, id=category_servers_id)


        if category_servers != None:
            print(f"The category {category_servers.name} already exists.")

        else:
            print(f"The category {category_name} does not yet exist and will now be created")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            
            }
        
            category_servers = await guild.create_category(category_name, overwrites=overwrites)
            print(f"The category {category_name} was created.")
            category_servers_id = category_servers.id
            write_config(config_dir, "category","category_servers_id", category_servers_id)

            was_created_list.append(category_servers)

# Creates a new text channel
        channel_name = "🌎-server-list"
        all_game_servers_channel_id = read_config(config_dir,"channel", "all_game_servers_channel_id", "int")
        all_game_servers_channel = discord.utils.get(guild.text_channels, id=all_game_servers_channel_id)

        if all_game_servers_channel != None:
            print(f"The channel 🌎-server-list already exists.")
        else:
            print(f"The channel {channel_name} does not exist.")
            all_game_servers_channel = await guild.create_text_channel(channel_name, category=category_servers)
            print(f"The channel {all_game_servers_channel.name} was created.")
            write_config(config_dir, "channel", "all_game_servers_channel_id", all_game_servers_channel.id)

            was_created_list.append(all_game_servers_channel)


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
            embed = discord.Embed(title=f"The following gameserver stats Channels have been created:",
                                description=f"> The following channels had to be created:\n{text}\ncreated: {dc_time}",
                                colour=0xffff80)
            try:
                bot_cmd_channel_id = read_config(config_dir, "channel", "bot_cmd_channel_id", "int")
                bot_cmd_channel = guild.get_channel(bot_cmd_channel_id)
                await bot_cmd_channel.send(embed=embed)
            except:
                pass


class bot_server_add(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    description = "Add a new server that fits into the routine"

    @app_commands.command(name="add_server", description=description)
    #@commands.has_any_role(1176145629412589619)
    @app_commands.describe(
            full_server_address ="{IP:PORT}",
        )
    async def server_add(self , interaction: discord.Interaction, full_server_address: str,):
        self.full_server_address = full_server_address

        data = get_server_data(steam_token, full_server_address)
        if data == None:

            embed = discord.Embed(title="your input is wrong",
                      description="use the command like this:\n```/add_server {ip_with_port}```\nExample:\n```/add_server full_server_address:213.239.210.121:27030```",
                      colour=0xff0000)
            interaction.response.send_message(embed=embed, ephemeral=True)

        try:
            name = data["response"]["servers"][0]["name"]
            data_true = True
        except:
            print(data)
            data_true = False

        if data_true == False:

            embed = discord.Embed(title="your input is wrong",
                description="use the command like this:\n```/add_server {ip_with_port}```\nExample:\n```/add_server full_server_address:213.239.210.121:27030```",
                colour=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if data_true == True:
            name = data["response"]["servers"][0]["name"]
            addr = data["response"]["servers"][0]["addr"]
            product = data["response"]["servers"][0]["product"]
            players = data["response"]["servers"][0]["players"]
            max_players = data["response"]["servers"][0]["max_players"]
            bots = data["response"]["servers"][0]["bots"]
            dedicated = data["response"]["servers"][0]["dedicated"]
            map = data["response"]["servers"][0]["map"]
            dc_timestemp = discord_time_convert(time.time())

            embed = discord.Embed(description=f"Address :  `{addr}`")

            embed.set_author(name=name)

            embed.add_field(name="Game",
                            value=f"`{product}`",
                            inline=False)
            embed.add_field(name="Players",
                            value=f"`{players}/{max_players}`",
                            inline=False)
            embed.add_field(name="Bots",
                            value=f"`{bots}`",
                            inline=False)
            embed.add_field(name="Map",
                            value=f"`{map}`",
                            inline=False)
            embed.add_field(name="Dedicated",
                            value=f"`{dedicated}`",
                            inline=False)
            embed.set_footer(text=f"update at {dc_timestemp}")

            view = Confirm_say()
            msg = await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

            await view.wait()
            if view.value is None:
                self.confirm_Button = False
                print(f'Timed out... self.confirm_Button = {self.confirm_Button}')
                embed = discord.Embed(title="Add a server command was cancelled",
                        description="If you want to try again you can do it with : \n```/add_server {ip_with_port}```\nExample:\n```/add_server full_server_address:213.239.210.121:27030```",
                        colour=0xff0000)

                await interaction.edit_original_response(embed=embed, view=None)

                # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

            elif view.value:
                self.confirm_Button = True
                print(f'Timed out... self.confirm_Button = {self.confirm_Button}')

                embed = discord.Embed(title="Successfully added!",
                        description=f"The server with the ip:\n```{full_server_address}```\nhas been added to the Discord bot and the required channels are now created for it.\nIf you want to delete it again, use the command :\n```/delt_server```",
                        colour=0xffff80)
                await interaction.edit_original_response(embed=embed, view=None)


                category_servers_id = read_config(config_dir,"category", "category_servers_id", "int")
                category_servers = discord.utils.get(interaction.guild.categories, id=category_servers_id)


                new_server_name_channel  = await interaction.guild.create_voice_channel(name=name, category=category_servers, overwrites={interaction.guild.default_role: discord.PermissionOverwrite(connect=False)})
                channel_name = f"🟢 Player: ({players}/{max_players})"
                new_server_stats_channel  = await interaction.guild.create_voice_channel(name=channel_name, category=category_servers, overwrites={interaction.guild.default_role: discord.PermissionOverwrite(connect=False)})

                all_game_servers_channel_id = read_config(config_dir,"channel", "all_game_servers_channel_id", "int")
                all_game_servers_channel = discord.utils.get(interaction.guild.text_channels, id=all_game_servers_channel_id)

                embed = discord.Embed(title="Placeholder up to the next server Discord routine", description=name)
                server_msg = await all_game_servers_channel.send(embed=embed)

                add_server_data(json_path_server_channel_data, full_server_address, name, new_server_name_channel.id, new_server_stats_channel.id, server_msg.id)


class server_stat_loops(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):

        self.bot = bot
        
        self.myLoop.start(bot)

    @tasks.loop(seconds=240)  # repeat after every 10 seconds
    async def myLoop(self, bot):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(guild_id)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Game Server Routine: {current_time}")


        data = read_json_file(json_path_server_channel_data)
        for key in data:
            
            server_address = data[key]["server_address"]
            server_data = get_server_data(steam_token, server_address)

            server_msg_id = data[key]["server_msg_id"]

            all_game_servers_channel_id = read_config(config_dir,"channel", "all_game_servers_channel_id", "int")
            all_game_servers_channel = discord.utils.get(guild.text_channels, id=all_game_servers_channel_id)

            server_msg = await all_game_servers_channel.fetch_message(server_msg_id)

            channel_stats_id = data[key]["channel_stats_id"]
            channel_stats = guild.get_channel(channel_stats_id)
        
            # channel_name_id = data[key]["channel_name_id"]
            # channel_name = guild.get_channel(channel_name_id)

            try: 
                name = server_data["response"]["servers"][0]["name"]
                addr = server_data["response"]["servers"][0]["addr"]
                product = server_data["response"]["servers"][0]["product"]
                players = server_data["response"]["servers"][0]["players"]
                max_players = server_data["response"]["servers"][0]["max_players"]
                bots = server_data["response"]["servers"][0]["bots"]
                dedicated = server_data["response"]["servers"][0]["dedicated"]
                map = server_data["response"]["servers"][0]["map"]
                dc_timestemp = discord_time_convert(time.time())

                channel_name_text = f"🟢 Player: ({players}/{max_players})"
                await channel_stats.edit(name = channel_name_text)


                embed = discord.Embed(title=name,
                                    description=f"Game Server Ip: `{server_address}`\n\ncs2 console join command:\n```connect {server_address}```\nBrwoser url to join the server directly:\n```steam://connect/{server_address}```\n> Player: **`{players}/{max_players}`** - Bots :**`{bots}`** \n\n*Updated* {dc_timestemp}")

                embed.set_author(name="Counter-Strike 2")

                embed.add_field(name="Game",
                                value=product,
                                inline=True)
                embed.add_field(name="Map",
                                value=map,
                                inline=True)
                embed.add_field(name="Dedicated",
                                value=dedicated,
                                inline=True)


                await server_msg.edit(embed=embed)

            except:
                print("\nSTEAM API ERROR\n:")
                print(server_data)
                print("\n")


# Confirm buttons
class Confirm_say(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button, ):
        await interaction.response.send_message('Confirming', ephemeral=True)
        print(f"Send Confrim / Cancel query.")

        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()



async def setup(bot: commands.Bot):
    await bot.add_cog(server_stats_system_setup(bot), guild=discord.Object(guild_id))
    await bot.add_cog(server_stat_loops(bot), guild=discord.Object(guild_id))
    await bot.add_cog(bot_server_add(bot), guild=discord.Object(guild_id))