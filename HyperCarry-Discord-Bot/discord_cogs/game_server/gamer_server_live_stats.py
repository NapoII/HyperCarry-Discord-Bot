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


        # Creates a new msg
        server_stats_list_msg_id = read_config(config_dir,"msg", "server_stats_list_msg_id", "int")
        try:
            server_stats_list_msg = await all_game_servers_channel.fetch_message(server_stats_list_msg_id)
            print(f"The channel server_stats_list_msg already exists.")
            
        except:
            embed = discord.Embed(title="Placeholder for the Server Stats list", description="list of server", color=0x00ff00)
            server_stats_list_msg = await all_game_servers_channel.send(embed=embed)
            write_config(config_dir, "msg", "server_stats_list_msg_id", server_stats_list_msg.id)


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

        key = check_ip_in_data(json_path_server_channel_data, full_server_address)
        print(f"/server_add --> Get used by {interaction.user.name} input: {full_server_address}")

        if key != False:
            await interaction.response.send_message(content=f"```{full_server_address}```\n**The Ip is already in the data set and will not be duplicated**\nplease enter an Ip that is not yet stored in the data!")
            print(f"/server_add --> The Ip is already in the data set and will not be duplicated: {full_server_address}")
        else:
            data = get_server_data(steam_token, full_server_address)

            if data == None:

                embed = discord.Embed(title="your input is wrong",
                        description="use the command like this:\n```/add_server {ip_with_port}```\nExample:\n```/add_server full_server_address:213.239.210.121:27030```",
                        colour=0xff0000)
                await interaction.response.defer()
                await interaction.channel.send(embed=embed)

            try:
                name = data["response"]["servers"][0]["name"]
                data_true = True
            except:
                print(data)
                data_true = False

            if data_true == False:
                await interaction.response.defer()
                print(f"/server_add --> input is wrong: {full_server_address}")

                embed = discord.Embed(title="your input is wrong",
                    description="use the command like this:\n```/add_server {ip_with_port}```\nExample:\n```/add_server full_server_address:213.239.210.121:27030```",
                    colour=0xff0000)
                await interaction.channel.send(embed=embed)

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
                print(f"/server_add --> Server entry is created: {full_server_address}")
                try:
                    await interaction.response.defer()
                except Exception as e:
                    print(f"\n\n/delt_server General error code:\n{e}\n")
                msg_server_test = await interaction.channel.send(embed=embed, view=view)

                await view.wait()
                if view.value is None:
                    self.confirm_Button = False

                    
                    print(f'Timed out... self.confirm_Button = {self.confirm_Button}')
                    print(f"/server_add --> command was cancelled: {full_server_address}")
                    embed = discord.Embed(title="Add a server command was cancelled",
                            description="If you want to try again you can do it with : \n```/add_server {ip_with_port}```\nExample:\n```/add_server full_server_address:213.239.210.121:27030```",
                            colour=0xff0000)
            
                    await msg_server_test.edit(embed=embed, view=None)
                    # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

                elif view.value:
                    self.confirm_Button = True
                    print(f'Timed out... self.confirm_Button = {self.confirm_Button}')
                    print(f"/server_add --> Successfully added: {msg_server_test.id}")
                    embed = discord.Embed(title="Successfully added!",
                            description=f"The server with the ip:\n```{full_server_address}```\nhas been added to the Discord bot and the required channels are now created for it.",
                            colour=0xffff80)
                    await msg_server_test.edit(embed=embed, view=None)


                    category_servers_id = read_config(config_dir,"category", "category_servers_id", "int")
                    category_servers = discord.utils.get(interaction.guild.categories, id=category_servers_id)

                    overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(connect=False, read_messages=True, view_channel=True ),  # Everyone can view and join the channel            
                }
                    new_server_name_channel  = await interaction.guild.create_voice_channel(name=name, category=category_servers, overwrites=overwrites)
                    channel_name = f"👥({players}/{max_players}) 🤖({bots})"
                    new_server_stats_channel  = await interaction.guild.create_voice_channel(name=channel_name, category=category_servers, overwrites=overwrites)

                    print(f"/server_add --> server_data: {full_server_address}, {name}, {new_server_name_channel.id}, { new_server_stats_channel.id}")
                    add_server_data(json_path_server_channel_data, full_server_address, name, new_server_name_channel.id, new_server_stats_channel.id)


class bot_server_delt(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    description = "Delt a new server from the routine"

    @app_commands.command(name="delt_server", description=description)
    #@commands.has_any_role(1176145629412589619)
    @app_commands.describe(
            full_server_address ="{IP:PORT}",
        )
    async def server_delt(self , interaction: discord.Interaction, full_server_address: str,):
        self.full_server_address = full_server_address

        print(f"/delt_server --> Get used by {interaction.user.name} input: {full_server_address}")
        await interaction.response.defer()
        key = check_ip_in_data(json_path_server_channel_data, full_server_address)

        if key == False:
            print(f"/delt_server --> ip was not found in the data input: {full_server_address}")

            addres_list = get_server_addresses(json_path_server_channel_data)

            text = ""
            for add in addres_list:
                text = text + f"\n```{add}```"
            
            content = f"```{full_server_address}```\n**The ip was not found in the data set and therefore cannot be deleted.**\nCheck it again by entering the right one.\n\n Active IPs\n{text}"
            embed = discord.Embed(title="wrong ip",
                      description=f"{content}",
                      colour=0xf40000)
            await interaction.channel.send(embed=embed)

        else:
            data = read_json_file(json_path_server_channel_data)

            channel_name_id = data[key]["channel_name_id"]
            channel_stats_id = data[key]["channel_stats_id"]

            try:
                channel_name = discord.utils.get(interaction.guild.voice_channels, id=channel_name_id)
                channel_stats = discord.utils.get(interaction.guild.voice_channels, id=channel_stats_id)

                print(f"/delt_server --> delt channel:{channel_name.name} - {channel_name.id}")
                await channel_name.delete()
                
                print(f"/delt_server --> delt channel:{channel_stats.name} - {channel_stats.id}")
                await channel_stats.delete()
                
                delete_entry(json_path_server_channel_data, key)

                content = f"The server with the ip: ```{full_server_address}``` was taken from the routine"
                embed = discord.Embed(title="wrong ip",
                      description=f"{content}",
                      colour=0x9cec09)
                await interaction.channel.send(embed=embed)

            except Exception as e:
                print(f"\n\n/delt_server General error code:\n{e}\n")



class server_stat_loops(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):

        self.bot = bot
        
        self.myLoop.start(bot)

    @tasks.loop(seconds=160)  # repeat after every 10 seconds #240
    async def myLoop(self, bot):
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(guild_id)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("\n")
        print(f"Game Server Routine --> {current_time}")


        all_game_servers_channel_id = read_config(config_dir,"channel", "all_game_servers_channel_id", "int")
        all_game_servers_channel = discord.utils.get(guild.text_channels, id=all_game_servers_channel_id)
            
        if all_game_servers_channel == None:
            
            channel_name = "🌎-server-list"
            print(f"Game Server Routine --> {channel_name} was not found and is now created {current_time}")
            try:
                all_game_servers_channel = await guild.create_text_channel(channel_name, category=category_servers)
                print(f"Game Server Routine --> channel created {all_game_servers_channel.id} {current_time}")
                write_config(config_dir, "channel", "all_game_servers_channel_id", all_game_servers_channel.id)
            
            except Exception as e:
                print(f"Game Server Routine --> ERROR {e}")
            

        data = read_json_file(json_path_server_channel_data)

        full_serverlist_text = ""

        for key in data:
            
            server_address = data[key]["server_address"]
            server_data = get_server_data(steam_token, server_address)

            channel_name_id = data[key]["channel_name_id"]
            channel_stats_id = data[key]["channel_stats_id"]
            channel_stats_id = data[key]["channel_stats_id"]

            server_name = data[key]["server_name"]

            channel_name = discord.utils.get(guild.voice_channels, id=channel_name_id)
            channel_stats = discord.utils.get(guild.voice_channels, id=channel_stats_id)

            if channel_name == None or channel_stats == None:
                print(f"Game Server Routine --> A channel is missing therefore all channels belonging to the server will be deleted and reloaded {current_time}")

                try:
                    await channel_name.delete()
                    print(f"Game Server Routine --> delt channel {channel_name.name} {current_time}")
                except:
                    pass

                try:
                    await channel_stats.delete()
                    print(f"Game Server Routine --> delt channel {channel_stats.name} {current_time}")
                except:
                    pass

                category_servers_id = read_config(config_dir,"category", "category_servers_id", "int")
                category_servers = discord.utils.get(guild.categories, id=category_servers_id)
                overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=False, read_messages=True, view_channel=True ),  # Everyone can view and join the channel            
            }
                channel_name = await guild.create_voice_channel(name=server_name, category=category_servers, overwrites=overwrites)
                channel_stats = await guild.create_voice_channel(name="Placeholder Server stats", category=category_servers, overwrites=overwrites)

                print(f"Game Server Routine --> Server channels are created {channel_name.name} - {channel_stats.name} - {current_time}")

                update_json(json_path_server_channel_data, key, "channel_name_id", channel_name.id, loaded_data=data)
                update_json(json_path_server_channel_data, key, "channel_stats_id", channel_stats.id, loaded_data=data)

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

                channel_name_text = f"👥({players}/{max_players}) 🤖({bots})"
                await channel_stats.edit(name = channel_name_text)
                print(f"Game Server Routine --> channel_stats update to {name} - {addr} - {channel_name_text}")

                full_serverlist_text = full_serverlist_text + f"""> ***{name}***
> Player:` {players}/{max_players}` | Bots: `{bots}` | map: `{map}`
> ```connect {addr}```\n\n"""
                await asyncio.sleep(10)

            except Exception as e:
                print(f"Game Server Routine --> STEAM API ERROR {server_name} - {server_address} - {current_time}")
                await asyncio.sleep(120)
                print(server_data)

            print("\n")


        # Creates a new msg
        server_stats_list_msg_id = read_config(config_dir,"msg", "server_stats_list_msg_id", "int")
        try:
            server_stats_list_msg = await all_game_servers_channel.fetch_message(server_stats_list_msg_id)
            
        except:
            embed = discord.Embed(title="Placeholder for the Server Stats list", description="list of server", color=0x00ff00)
            server_stats_list_msg = await all_game_servers_channel.send(embed=embed)
            write_config(config_dir, "msg", "server_stats_list_msg_id", server_stats_list_msg.id)

        dc_timecode = discord_time_convert(time.time())
        embed = discord.Embed(title="HyperCarry server list",
                      description=f"{full_serverlist_text}\nupdate {dc_timecode}",
                      colour=0xb97a3c)
        await server_stats_list_msg.edit(embed=embed)


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
    await bot.add_cog(bot_server_delt(bot), guild=discord.Object(guild_id))