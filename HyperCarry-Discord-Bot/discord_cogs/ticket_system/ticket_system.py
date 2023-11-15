"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This COG is for embed a help information for Rust.
exampel : cctv codes
------------------------------------------------
"""

from discord.ext import commands, tasks
from util.__funktion__ import *
import random
import discord
from discord import app_commands
from discord import app_commands, ui
from discord import Color
import asyncio

# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")
category_private_voice_id = int(read_config(config_dir, "category", "category_private_voice_id"))
json_path = os.path.join(current_dir, "ticket_data.json")
json_path_support = os.path.join(current_dir, "support_team_data.json")

guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1


create_channel_id =  read_config(config_dir, "channel", "create_channel_id", "int")

if create_channel_id == None:
    create_channel_id = 1

category_private_voice_id = read_config(config_dir, "category", "category_private_voice_id", "int")
if category_private_voice_id == None:
    category_private_voice_id = 1


class ticket_system_setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir  # Beispiel-Konfigurationsverzeichnis


        # Hier wird die Methode beim Start des Bots aufgerufen
        self.bot.loop.create_task(self.setup_ticket_system())

    async def setup_ticket_system(self):
        print ("\n --> setup_ticket_system\n")
        await self.bot.wait_until_ready()  # Warte, bis der Bot vollständig gestartet ist
        guild = self.bot.get_guild(guild_id)  # Ersetze YOUR_GUILD_ID durch die tatsächliche Guild-ID


        was_created_list = []


# Creates a new Role
        role_name = "💼-support-team"
        role_colour = discord.Color.from_rgb(255, 255, 255)
        support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")
        support_team_role = discord.utils.get(guild.roles, id=support_team_role_id)

        if support_team_role != None:
            print(f"The role {support_team_role.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            support_team_role = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {support_team_role.name} was created.")
            write_config(config_dir, "role", "support_team_role_id", support_team_role.id)


# Creates a new Role
        role_name = "💼-aktiv-support-team"
        role_colour = discord.Color.from_rgb(189, 152, 255)
        aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
        aktiv_support_team_role = discord.utils.get(guild.roles, id=aktiv_support_team_role_id)

        if aktiv_support_team_role != None:
            print(f"The role {aktiv_support_team_role.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            aktiv_support_team_role = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {aktiv_support_team_role.name} was created.")
            write_config(config_dir, "role", "aktiv_support_team_role_id", aktiv_support_team_role.id)


# Creates a new category
        category_name = "------ 👮 - Support - 👮 ------"
        category_support_id = read_config(config_dir,"category", "category_support_id", "int")
        category_support = discord.utils.get(guild.categories, id=category_support_id)


        if category_support != None:
            print(f"The category {category_support.name} already exists.")

        else:
            print(f"The category {category_name} does not yet exist and will now be created")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }
        
            category_support = await guild.create_category(category_name, overwrites=overwrites)
            print(f"The category {category_name} was created.")
            category_support_id = category_support.id
            write_config(config_dir, "category","category_support_id", category_support_id)

            was_created_list.append(category_support)



# Creates a new text channel
        channel_name = "📂-open-a-ticket"
        open_a_ticket_channel_id = read_config(config_dir,"channel", "open_a_ticket_channel_id", "int")
        open_a_ticket_channel = discord.utils.get(guild.text_channels, id=open_a_ticket_channel_id)

        if open_a_ticket_channel != None:
            print(f"The channel {open_a_ticket_channel.name} already exists.")
        else:
            print(f"The channel {channel_name} does not exist.")
            open_a_ticket_channel = await guild.create_text_channel(channel_name, category=category_support)
            print(f"The channel {open_a_ticket_channel.name} was created.")
            write_config(config_dir, "channel", "open_a_ticket_channel_id", open_a_ticket_channel.id)

            was_created_list.append(open_a_ticket_channel)



# Creates a new msg
        open_a_ticket_msg_id = read_config(config_dir,"msg", "open_a_ticket_msg_id", "int")
        try:
            open_a_ticket_msg = await open_a_ticket_channel.fetch_message(open_a_ticket_msg_id)
            print(f"The channel open_a_ticket_msg already exists.")
            
        except:
            embed = discord.Embed(title="Hyper-Carry - Support System",
                      description="Please click the most relevant button to your issue below and answer the messages sent to you to the best of your ability.\n\n**Please make sure your DMs are turned on as the bot will DM you your questions!**\n\n> **🚨 Report Player 🚨**\n> Use this ticket type to report a player for breaking the rules.",
                      colour=0xffffff)
            open_a_ticket_msg = await open_a_ticket_channel.send(embed=embed, view=ticket_button())
            write_config(config_dir, "msg", "open_a_ticket_msg_id", open_a_ticket_msg.id)



# Creates a new text channel
        channel_name = "💼-support-team"
        support_team_channel_id = read_config(config_dir,"channel", "support_team_channel_id", "int")
        support_team_channel = discord.utils.get(guild.text_channels, id=support_team_channel_id)

        if support_team_channel != None:
            print(f"The channel {support_team_channel.name} already exists.")
        else:
            print(f"The channel {channel_name} does not exist.")
            support_team_channel = await guild.create_text_channel(channel_name, category=category_support)
            await support_team_channel.set_permissions(guild.default_role, read_messages=False)
            await support_team_channel.set_permissions(support_team_role, send_messages=False, read_messages=True)
            print(f"The channel {support_team_channel.name} was created.")
            write_config(config_dir, "channel", "support_team_channel_id", support_team_channel.id)

            was_created_list.append(support_team_channel)



# Creates a new msg
        support_team_msg_id = read_config(config_dir,"msg", "support_team_msg_id", "int")
        try:
            support_team_msg = await support_team_channel.fetch_message(support_team_msg_id)
            print(f"The channel support_team_msg already exists.")
            
        except:
            embed = discord.Embed(title="Space holder for Ticket msg", description="The Support Team System window", color=0x00ff00)
            support_team_msg = await support_team_channel.send(embed=embed, view=support_team_button())
            write_config(config_dir, "msg", "support_team_msg_id", support_team_msg.id)



# Creates a new category
        category_name = "-----📚-ticket-archiv-📚-----"
        category_ticket_archiv = discord.utils.get(guild.categories, name=category_name)

        if category_ticket_archiv != None:
            print(f"The category {category_ticket_archiv.name} already exists.")

        else:
            print(f"The category {category_name} does not yet exist and will now be created")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=False, read_messages=True, manage_channels=False),  # The bot can send messages, others can only view
                support_team_role: discord.PermissionOverwrite(manage_messages=True, view_guild_insights=True, read_message_history=True, view_channel=True, read_messages=True, send_messages=False, connect=False, speak=False)
            }


        
            category_ticket_archiv = await guild.create_category(category_name, overwrites=overwrites)
            print(f"The category {category_name} was created.")
            category_ticket_archiv_id = category_ticket_archiv.id
            write_config(config_dir, "category","category_ticket_archiv_id", category_ticket_archiv_id)

            was_created_list.append(category_ticket_archiv)



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
            embed = discord.Embed(title=f"The following Ticket System Channels have been created:",
                                description=f"> The following channels had to be created:\n{text}\ncreated: {dc_time}",
                                colour=0xffff80)
            try:
                bot_cmd_channel_id = read_config(config_dir, "channel", "bot_cmd_channel_id", "int")
                bot_cmd_channel = guild.get_channel(bot_cmd_channel_id)
                await bot_cmd_channel.send(embed=embed)
            except:
                pass



# new button
class support_team_button(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="Support Cheack In", style=discord.ButtonStyle.green, custom_id="cheack_in")
    async def cheack_in(self, interaction: discord.Interaction, Button: discord.ui.Button):

        timestemp = time.time()
        discord_time_str = discord_time_convert(timestemp)
        aktiv_support_team_role_id = read_config(config_dir, "role", "aktiv_support_team_role_id", "int")
        support_team_channel_id = read_config(config_dir, "channel", "support_team_channel_id", "int")
        aktiv_support_team_role = interaction.guild.get_role(aktiv_support_team_role_id)
        support_team_role = interaction.guild.get_role(aktiv_support_team_role_id)

        if support_team_role:

            if not support_team_role in interaction.user.roles:
                await interaction.response.defer(ephemeral=True)
                await interaction.user.add_roles(support_team_role)
                description = f"""When a new ticket has opened, I will inform you here by pm.
                
                You can check out again in the following channel:
                <#{support_team_channel_id}>
                
                **You are checked in** {discord_time_str}
                """
                embed = discord.Embed(title="💼 You have checked in as an  Aktiv-Support-Team 💼",
                            description=description,
                            colour=0x80ff80)
                await interaction.user.send(embed=embed)

                support_entry_in_data(json_path_support, timestemp, interaction.user.name, interaction.user.id)

                text = support_dashboard_text(json_path, interaction.guild.members, aktiv_support_team_role, support_team_role)
                embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                    description=text,
                                    colour=0xffffff)
                await interaction.message.edit(embed=embed)


            else:
                embed = discord.Embed(title="💼 You are already checked in to the active support team💼",
                      colour=0xff0000)
                await interaction.response.send_message(embed=embed, ephemeral=True)


    
    @discord.ui.button(label="Support Cheack Out", style=discord.ButtonStyle.red, custom_id="cheack_out")
    async def cheack_out(self, interaction: discord.Interaction, Button: discord.ui.Button):

        timestemp = time.time()
        discord_time_str = discord_time_convert(timestemp)
        aktiv_support_team_role_id = read_config(config_dir, "role", "aktiv_support_team_role_id", "int")
        support_team_role_id = read_config(config_dir, "role", "support_team_role_id", "int")
        support_team_channel_id = read_config(config_dir, "channel", "support_team_channel_id", "int")

        support_team_role = interaction.guild.get_role(support_team_role_id)
        aktiv_support_team_role = interaction.guild.get_role(aktiv_support_team_role_id)

        if aktiv_support_team_role:
            if aktiv_support_team_role in interaction.user.roles:

                await interaction.response.defer(ephemeral=True)
                await interaction.user.remove_roles(aktiv_support_team_role)

                description = f"""You will no longer be notified when a new ticket is opened.
                
                You can check in again in the following channel:
                <#{support_team_channel_id}>
                
                **You are checked out** {discord_time_str}
                """
                embed = discord.Embed(title="💼 You have checked out as an  Aktiv-Support-Team 💼",
                            description=description,
                            colour=0x80ff80)
                await interaction.user.send(embed=embed)

                support_update_check_out(json_path=json_path_support, user_id=interaction.user.id, timestamp=timestemp)
                
                text = support_dashboard_text(json_path, interaction.guild.members, aktiv_support_team_role, support_team_role)
                embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                    description=text,
                                    colour=0xffffff)
                await interaction.message.edit(embed=embed)

            else:
                embed = discord.Embed(title="💼 You are not checked in for now in to the active support team💼",
                      colour=0xff0000)
                await interaction.response.send_message(embed=embed, ephemeral=True)


# new button
class ticket_button(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="🚨 Report Player 🚨", style=discord.ButtonStyle.red, custom_id="report")
    async def report_player(self, interaction: discord.Interaction, Button: discord.ui.Button):
        thumbnail = "https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png"

        user = interaction.user
        user_id = interaction.user.id
        data = read_json_file(json_path)

        guild_id = read_config(config_dir,"client", "guild_id", "int")

        if is_user_id_in_data(data, user_id) == True:
            key = find_key_by_user_id(data, user_id)
            ticket_channel_id = data[key]["ticket_channel_id"]
            unix_timestemp = data[key]["unix_timestemp"]
            discord_time = discord_time_convert(unix_timestemp)
            embed = discord.Embed(title="You already have a ticket open",
                      description=f"<#{ticket_channel_id}> {discord_time}",
                      colour=0xff0000)
            await interaction.response.defer(ephemeral=True)
            await interaction.user.send(embed=embed)

        else:
            text_1 = "Thank you for using our reporting system! To expedite the resolution process, we kindly request you to answer six essential questions before our team addresses your report. If you change your mind, you can cancel the report with !stop, or it will automatically expire after 10 minutes without a response."
            embed = discord.Embed(title="🚨 Report Player 🚨",
                                description=text_1,
                                colour=0xf40006)
            embed.set_author(name="👮 Your personal support agent👮")
            embed.set_thumbnail(url=thumbnail)
            await interaction.response.defer(ephemeral=True)
            await interaction.user.send(embed=embed)


            answers = []
            questions = [
            "What is the name of the player you are reporting, or do you have a link to their Steam profile?",
            "Please provide your Steam name or Steam profile link.",
            "Which server do you want to report the player on?",
            "What specific actions or behavior are you reporting the player for? Please provide details.",
            "Do you have any evidence to support your report, such as video recordings, demo, screenshots, or other documentation?",
            "Is there any additional information you would like to share before our team investigates the matter?"
        ]
            
            for question in questions:
                embed = discord.Embed(title=f"{question}", colour=0x80ffff)
                await interaction.user.send(embed=embed)

                def check(m):
                    return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)

                try:
                    # Wait for user's response for up to 10 minutes
                    response = await interaction.client.wait_for('message', check=check, timeout=600)
                except asyncio.TimeoutError:
                    
                    open_a_ticket_channel_id = read_config(config_dir,"channel", "open_a_ticket_channel_id", "int")
                    text = f""" we assume the problem is resolved.
                                        We've closed your ticket. If the issue persists,
                                        feel free to open a new ticket in the channel
                                        <#{open_a_ticket_channel_id}>
                                        And we'll be happy to help."""
                    embed = discord.Embed(title=f"Since we didn't hear back from you," ,description =text, colour=0xf40006)
                    await interaction.user.send(embed=embed)
                    return

                answers.append(response.content)

            ticket_num = len(data)+1        
            ticket_type = "player report"
            user_name = interaction.user.name
            user_id = interaction.user.id
            unix_timestemp = time.time()
            ticket_status = "open"

            channel_name = f"📝-{user_name}-ticket-{ticket_num}"
            category_support_id = read_config(config_dir,"category", "category_support_id", "int")
            category_support = discord.utils.get(interaction.guild.categories, id=category_support_id)
            guild = interaction.client.get_guild(guild_id)
            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")

            support_team_role = guild.get_role(support_team_role_id)
            role_colour = discord.Color.from_rgb(0, 0, 0)
            ticket_role = await guild.create_role(name=channel_name, colour=role_colour)
            await interaction.user.add_roles(ticket_role)

            ticket = await interaction.guild.create_text_channel(channel_name, category=category_support)
            await ticket.set_permissions(guild.default_role, read_messages=False)
            await ticket.set_permissions(ticket_role, send_messages=False, read_messages=True)
            await ticket.set_permissions(support_team_role, send_messages=False, read_messages=True)
            
            add_new_ticket_data(json_path, ticket_num, ticket_type, user_name, user_id, ticket.id, unix_timestemp, ticket_status)
            print(f"The channel {ticket.name} was created.")

            
            confirmation_message = "🌟 Thank you for providing the information 🌟"
            text = f"""Your report has been submitted for review. Our team will investigate the matter and take appropriate action.
            A ticket channel has been set up for you, where our support will take care of your request for you.
            
            <#{ticket.id}>"""
            embed = discord.Embed(title=f"{confirmation_message}", description=f"{text}", colour=0x0080ff)

            embed.set_author(name="🚨 Report Player 🚨")
            await interaction.user.send(embed=embed)

            
            support_team_channel_id = read_config(config_dir,"channel", "support_team_channel_id", "int")
            support_team_msg_id = read_config(config_dir,"msg", "support_team_msg_id", "int")
            

            support_team_channel = guild.get_channel(support_team_channel_id)
            support_team_msg = await support_team_channel.fetch_message(support_team_msg_id)


            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")
            support_team_role = discord.utils.get(interaction.guild.roles, id=support_team_role_id)
            aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
            aktiv_support_team_role = discord.utils.get(interaction.guild.roles, id=aktiv_support_team_role_id)
            
            text = support_dashboard_text(json_path, interaction.guild.members, aktiv_support_team_role, support_team_role)
            embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                description=text,
                                colour=0xffffff)
            await support_team_msg.edit(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ticket_system_setup(bot), guild=discord.Object(guild_id))
    bot.add_view(ticket_button())
    bot.add_view(support_team_button())
 




"""        text_2 = "What is the name of the player you are reporting, or do you have a link to their Steam profile?"
        text_3 = "Please provide your Steam name or Steam profile link."
        text_4 = "Which server do you want to report the player on?"
        text_5 = "What specific actions or behavior are you reporting the player for? Please provide details."
        text_6 = "Do you have any evidence to support your report, such as video recordings, demo, screenshots, or other documentation?"
        text_7 = "Is there any additional information you would like to share before our team investigates the matter?"
"""

