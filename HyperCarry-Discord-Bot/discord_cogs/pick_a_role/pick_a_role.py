"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
Pick a Role:
The user can select some game roles with buttons and see the channel for the rules.
------------------------------------------------
"""

from discord.app_commands import Choice
from util.__funktion__ import *

from discord.ext import commands, tasks
from util.__funktion__ import *
import random
import discord
from discord import app_commands
from discord import app_commands, ui

current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")


guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1


class pick_a_role_setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir

        self.bot.loop.create_task(self.setup_channel_hopper())

    async def setup_channel_hopper(self):
        print ("\n --> setup_pick_a_role\n")
        await self.bot.wait_until_ready()  
        guild = self.bot.get_guild(guild_id)  

        was_created_list=[]


# Creates a new category
        category_name = "-------- 🎮- Games -🎮--------"
        category_games_id = read_config(config_dir,"category", "category_games_id", "int")
        category_games = discord.utils.get(guild.categories, id=category_games_id)


        if category_games != None:
            print(f"The category {category_games.name} already exists.")

        else:
            print(f"The category {category_name} does not yet exist and will now be created")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            
            }
        
            category_games = await guild.create_category(category_name, overwrites=overwrites)
            print(f"The category {category_name} was created.")
            category_games_id = category_games.id
            write_config(config_dir, "category","category_games_id", category_games_id)

            was_created_list.append(category_games)


# Creates a new text channel
        channel_name = "📜-roles-n-rules"
        roles_n_rules_channel_id = read_config(config_dir,"channel", "roles_n_rules_channel_id", "int")
        roles_n_rules_channel = discord.utils.get(guild.text_channels, id=roles_n_rules_channel_id)

        if roles_n_rules_channel != None:
            print(f"The channel roles-n-rules already exists.")
        else:
            print(f"The channel {channel_name} does not exist.")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            
            }
            roles_n_rules_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
            print(f"The channel {roles_n_rules_channel.name} was created.")
            write_config(config_dir, "channel", "roles_n_rules_channel_id", roles_n_rules_channel.id)

            was_created_list.append(roles_n_rules_channel)


# Creates a new msg
        pick_a_role_msg_id = read_config(config_dir,"msg", "pick_a_role_msg_id", "int")
        try:
            pick_a_role_msg = await roles_n_rules_channel.fetch_message(pick_a_role_msg_id)
            print(f"The channel pick_a_role_msg already exists.")
            
        except:

            text = """**🔒 Channel Access Roles**

Welcome to our Discord server! To enhance your experience and provide a streamlined environment, we've implemented Channel Access Roles. These roles grant you access to specific channels, allowing you to focus on the content that matters most to you.

**How it works:**
- Below this message, you'll find interactive buttons corresponding to different channels or topics.
- By clicking on a button, you'll be assigned a role associated with that channel.
- Each role grants access to a specific set of channels related to the chosen topic.
- This helps you declutter your view, ensuring that you only see the channels that interest you.

**Note:**
- You can customize your experience at any time by clicking and unclicking the buttons.
- If you have any questions or need assistance, feel free to reach out to our friendly staff.

Enjoy your time on our server, and happy chatting!

> **🎮 Counter Strike 2 🎮**
> Pick the role for cs2

> **⚽ Rocket League ⚽**
> Pick the role for RL

> **🦕 Ark 🦕**
> Pick the role for ark

> **🚀 Among Us 🚀**
> Pick the role for among us

> **🩸 Back 4 Blood 🩸**
> Pick the role for back4blood

"""

            description= text
            embed = discord.Embed(title="Hyper-Carry - Pick a Role", description= description, colour=0xffffff)
            pick_a_role_msg = await roles_n_rules_channel.send(embed=embed, view=pick_a_role_button())
            write_config(config_dir, "msg", "pick_a_role_msg_id", pick_a_role_msg.id)


# Creates a new Role
        role_name = "🎮-counter-strike-2"
        role_colour = discord.Color.dark_gold()
        counter_strike_2_role_id = read_config(config_dir,"role", "counter_strike_2_role_id", "int")
        counter_strike_2_role = discord.utils.get(guild.roles, id = counter_strike_2_role_id)

        if counter_strike_2_role != None:
            print(f"The role {counter_strike_2_role.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            counter_strike_2_role = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {counter_strike_2_role.name} was created.")
            write_config(config_dir, "role", "counter_strike_2_role_id", counter_strike_2_role.id)


# Creates a new text channel
        channel_name = "🎮-counter-strike-2"
        counter_strike_2_channel_id = read_config(config_dir,"channel", "counter_strike_2_channel_id", "int")
        counter_strike_2_channel = discord.utils.get(guild.text_channels, id=counter_strike_2_channel_id)

        if counter_strike_2_channel != None:
            print(f"The channel roles-n-rules already exists.")
        else:
            print(f"The channel {channel_name} does not exist.")
            counter_strike_2_channel = await guild.create_text_channel(channel_name, category=category_games)
            await counter_strike_2_channel.set_permissions(guild.default_role, read_messages=False)
            await counter_strike_2_channel.set_permissions(counter_strike_2_role, read_messages=True)
            print(f"The channel {counter_strike_2_channel.name} was created.")
            write_config(config_dir, "channel", "counter_strike_2_channel_id", counter_strike_2_channel.id)

            was_created_list.append(counter_strike_2_channel)


# Creates a new Role
        role_name = "🩸-back4blood"
        role_colour = discord.Color.red()
        back4blood_role_id = read_config(config_dir,"role", "back_4_blood_role_id", "int")
        back4blood_role = discord.utils.get(guild.roles, id = back4blood_role_id)

        if back4blood_role != None:
            print(f"The role {back4blood_role.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            back4blood_role = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {back4blood_role.name} was created.")
            write_config(config_dir, "role", "back_4_blood_role_id", back4blood_role.id)


# Creates a new text channel
        channel_name = "🩸-back4blood"
        back4blood_channel_id = read_config(config_dir,"channel", "back4blood_channel_id", "int")
        back4blood_channel = discord.utils.get(guild.text_channels, id=back4blood_channel_id)

        if back4blood_channel != None:
            print(f"The channel roles-n-rules already exists.")
        else:
            print(f"The channel {channel_name} does not exist.")
            back4blood_channel = await guild.create_text_channel(channel_name, category=category_games)
            await back4blood_channel.set_permissions(guild.default_role, read_messages=False)
            await back4blood_channel.set_permissions(back4blood_role, read_messages=True)
            print(f"The channel {back4blood_channel.name} was created.")
            write_config(config_dir, "channel", "back4blood_channel_id", back4blood_channel.id)

            was_created_list.append(back4blood_channel)



# Creates a new Role
        role_name = "⚽-rocket-league"
        role_colour = discord.Color.dark_blue()
        rocket_league_role_id = read_config(config_dir,"role", "rocket_league_role_id", "int")
        rocket_league_role = discord.utils.get(guild.roles, id = rocket_league_role_id)

        if rocket_league_role != None:
            print(f"The role {rocket_league_role.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            rocket_league_role = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {rocket_league_role.name} was created.")
            write_config(config_dir, "role", "rocket_league_role_id", rocket_league_role.id)


# Creates a new text channel
        channel_name = "⚽-rocket-league"
        rocket_league_channel_id = read_config(config_dir,"channel", "rocket_league_channel_id", "int")
        rocket_league_channel = discord.utils.get(guild.text_channels, id=rocket_league_channel_id)

        if rocket_league_channel != None:
            print(f"The channel roles-n-rules already exists.")
        else:
            print(f"The channel {channel_name} does not exist.")
            rocket_league_channel = await guild.create_text_channel(channel_name, category=category_games)
            await rocket_league_channel.set_permissions(guild.default_role, read_messages=False)
            await rocket_league_channel.set_permissions(rocket_league_role, read_messages=True)
            print(f"The channel {rocket_league_channel.name} was created.")
            write_config(config_dir, "channel", "rocket_league_channel_id", rocket_league_channel.id)

            was_created_list.append(rocket_league_channel)


# Creates a new Role
        role_name = "🦕-ark"
        role_colour = discord.Color.green()
        ark_role_id = read_config(config_dir,"role", "ark_role_id", "int")
        ark_role = discord.utils.get(guild.roles, id = ark_role_id)

        if ark_role != None:
            print(f"The role {ark_role.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            ark_role = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {ark_role.name} was created.")
            write_config(config_dir, "role", "ark_role_id", ark_role.id)


# Creates a new text channel
        channel_name = "🦕-ark"
        ark_channel_id = read_config(config_dir,"channel", "ark_channel_id", "int")
        ark_channel = discord.utils.get(guild.text_channels, id=ark_channel_id)

        if ark_channel != None:
            print(f"The channel roles-n-rules already exists.")
        else:
            print(f"The channel {channel_name} does not exist.")
            ark_channel = await guild.create_text_channel(channel_name, category=category_games)
            await ark_channel.set_permissions(guild.default_role, read_messages=False)
            await ark_channel.set_permissions(ark_role, read_messages=True)
            print(f"The channel {ark_channel.name} was created.")
            write_config(config_dir, "channel", "ark_channel_id", ark_channel.id)

            was_created_list.append(ark_channel)


# Creates a new Role
        role_name = "🚀-among-us"
        role_colour = discord.Color.from_rgb(168,67,0)
        among_us_role_id = read_config(config_dir,"role", "among_us_role_id", "int")
        among_us_role = discord.utils.get(guild.roles, id = among_us_role_id)

        if among_us_role != None:
            print(f"The role {among_us_role.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            among_us_role = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {among_us_role.name} was created.")
            write_config(config_dir, "role", "among_us_role_id", among_us_role.id)


# Creates a new text channel
        channel_name = "🚀-among-us"
        among_us_channel_id = read_config(config_dir,"channel", "among_us_channel_id", "int")
        among_us_channel = discord.utils.get(guild.text_channels, id=among_us_channel_id)

        if among_us_channel != None:
            print(f"The channel roles-n-rules already exists.")
        else:
            print(f"The channel {channel_name} does not exist.")
            among_us_channel = await guild.create_text_channel(channel_name, category=category_games)
            await among_us_channel.set_permissions(guild.default_role, read_messages=False)
            await among_us_channel.set_permissions(among_us_role, read_messages=True)
            print(f"The channel {among_us_channel.name} was created.")
            write_config(config_dir, "channel", "among_us_channel_id", among_us_channel.id)

            was_created_list.append(among_us_channel)



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
            embed = discord.Embed(title=f"The following Pick a role channels have been created:",
                                description=f"> The following channels had to be created:\n{text}\ncreated: {dc_time}",
                                colour=0xffff80)
            try:
                bot_cmd_channel_id = read_config(config_dir, "channel", "bot_cmd_channel_id", "int")
                bot_cmd_channel = guild.get_channel(bot_cmd_channel_id)
                await bot_cmd_channel.send(embed=embed)
            except:
                pass


# new button
class pick_a_role_button(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="🎮 Counter Strike 2 🎮", style=discord.ButtonStyle.secondary, custom_id="cs2_role_pic")
    async def cs2_role(self, interaction: discord.Interaction, Button: discord.ui.Button):
        print(f"pick_a_role_button [🎮 Counter Strike 2 🎮] --> get used by {interaction.user.name}")
        user_roles = interaction.user.roles
        counter_strike_2_role_id = read_config(config_dir,"role", "counter_strike_2_role_id", "int")
        counter_strike_2_role = discord.utils.get(interaction.guild.roles, id = counter_strike_2_role_id)

        user_role_id_list = []
        for role in user_roles:
            user_role_id_list.append(role.id)
        
        if counter_strike_2_role.id not in user_role_id_list:
            
            print(f"pick_a_role_button [🎮 Counter Strike 2 🎮] --> add user the role {counter_strike_2_role.name}")
            await interaction.user.add_roles(counter_strike_2_role)
            embed = discord.Embed(title="You have added a new role.",
                      description=f"<@&{counter_strike_2_role.id}>",
                      colour=0x80ff00)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if counter_strike_2_role.id in user_role_id_list:
            print(f"pick_a_role_button [🎮 Counter Strike 2 🎮] --> delt user from the role {counter_strike_2_role.name}")

            await interaction.user.remove_roles(counter_strike_2_role)
            embed = discord.Embed(title="You have remove a role.",
                      description=f"<@&{counter_strike_2_role.id}>",
                      colour=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @discord.ui.button(label="⚽ Rocket League ⚽", style=discord.ButtonStyle.secondary, custom_id="rl_role_pic")
    async def rl_role(self, interaction: discord.Interaction, Button: discord.ui.Button):

        print(f"pick_a_role_button [⚽ Rocket League ⚽] --> get used by {interaction.user.name}")
        user_roles = interaction.user.roles
        rocket_league_role_id = read_config(config_dir,"role", "rocket_league_role_id", "int")
        rocket_league_role = discord.utils.get(interaction.guild.roles, id = rocket_league_role_id)

        user_role_id_list = []
        for role in user_roles:
            user_role_id_list.append(role.id)
        
        if rocket_league_role.id not in user_role_id_list:
            print(f"pick_a_role_button [⚽ Rocket League ⚽] --> add user the role {rocket_league_role.name}")
            await interaction.user.add_roles(rocket_league_role)
            embed = discord.Embed(title="You have added a new role.",
                      description=f"<@&{rocket_league_role.id}>",
                      colour=0x80ff00)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if rocket_league_role.id in user_role_id_list:
            print(f"pick_a_role_button [⚽ Rocket League ⚽] --> delt user from the role {rocket_league_role.name}")
            await interaction.user.remove_roles(rocket_league_role)
            embed = discord.Embed(title="You have remove a role.",
                      description=f"<@&{rocket_league_role.id}>",
                      colour=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @discord.ui.button(label="🦕 Ark 🦕", style=discord.ButtonStyle.secondary, custom_id="ark_role_pic")
    async def ark_role(self, interaction: discord.Interaction, Button: discord.ui.Button):
        print(f"pick_a_role_button [🦕 Ark 🦕] --> get used by {interaction.user.name}")
        user_roles = interaction.user.roles
        ark_role_id = read_config(config_dir,"role", "ark_role_id", "int")
        ark_role = discord.utils.get(interaction.guild.roles, id = ark_role_id)

        user_role_id_list = []
        for role in user_roles:
            user_role_id_list.append(role.id)
        
        if ark_role.id not in user_role_id_list:
            print(f"pick_a_role_button [🦕 Ark 🦕] --> add user the role {ark_role.name}")
            await interaction.user.add_roles(ark_role)
            embed = discord.Embed(title="You have added a new role.",
                      description=f"<@&{ark_role.id}>",
                      colour=0x80ff00)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if ark_role.id in user_role_id_list:
            print(f"pick_a_role_button [🦕 Ark 🦕] --> delt user from the role {ark_role.name}")
            await interaction.user.remove_roles(ark_role)
            embed = discord.Embed(title="You have remove a role.",
                      description=f"<@&{ark_role.id}>",
                      colour=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @discord.ui.button(label="🚀 Among Us 🚀", style=discord.ButtonStyle.secondary, custom_id="among_us_role_pic")
    async def among_us_role(self, interaction: discord.Interaction, Button: discord.ui.Button):
        print(f"pick_a_role_button [🚀 Among Us 🚀] --> get used by {interaction.user.name}")
        user_roles = interaction.user.roles
        among_us_role_id = read_config(config_dir,"role", "among_us_role_id", "int")
        among_us_role = discord.utils.get(interaction.guild.roles, id = among_us_role_id)

        user_role_id_list = []
        for role in user_roles:
            user_role_id_list.append(role.id)
        
        if among_us_role.id not in user_role_id_list:
            print(f"pick_a_role_button [🚀 Among Us 🚀] --> add user the role {among_us_role.name}")
            await interaction.user.add_roles(among_us_role)
            embed = discord.Embed(title="You have added a new role.",
                      description=f"<@&{among_us_role.id}>",
                      colour=0x80ff00)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if among_us_role.id in user_role_id_list:
            print(f"pick_a_role_button [🚀 Among Us 🚀] --> delt user from the role {among_us_role.name}")
            await interaction.user.remove_roles(among_us_role)
            embed = discord.Embed(title="You have remove a role.",
                      description=f"<@&{among_us_role.id}>",
                      colour=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @discord.ui.button(label="🩸 Back 4 Blood 🩸", style=discord.ButtonStyle.secondary, custom_id="back_4_blood_role_pic")
    async def back_4_blood_role(self, interaction: discord.Interaction, Button: discord.ui.Button):
        print(f"pick_a_role_button [🩸 Back 4 Blood 🩸] --> get used by {interaction.user.name}")
        user_roles = interaction.user.roles
        
        back_4_blood_role_id = read_config(config_dir,"role", "back_4_blood_role_id", "int")
        back_4_blood_role = discord.utils.get(interaction.guild.roles, id = back_4_blood_role_id)

        user_role_id_list = []
        for role in user_roles:
            user_role_id_list.append(role.id)
        
        if back_4_blood_role.id not in user_role_id_list:
            print(f"pick_a_role_button [🩸 Back 4 Blood 🩸] --> add user the role {back_4_blood_role.name}")
            await interaction.user.add_roles(back_4_blood_role)
            embed = discord.Embed(title="You have added a new role.",
                      description=f"<@&{back_4_blood_role.id}>",
                      colour=0x80ff00)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if back_4_blood_role.id in user_role_id_list:
            print(f"pick_a_role_button [🩸 Back 4 Blood 🩸] --> delt user from the role {back_4_blood_role.name}")
            await interaction.user.remove_roles(back_4_blood_role)
            embed = discord.Embed(title="You have remove a role.",
                      description=f"<@&{back_4_blood_role.id}>",
                      colour=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(pick_a_role_setup(bot), guild=discord.Object(guild_id))
    bot.add_view(pick_a_role_button())