"""Full Doku on: https://github.com/NapoII"
-----------------------------------------------
Ticket System brend with HC discord
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

json_path_ticket = os.path.join(current_dir, "ticket_data.json")
json_path_support = os.path.join(current_dir, "support_team_data.json")
ticket_aktion_id_dir = os.path.join(current_dir, "ticket_aktion.id")


guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1



class ticket_system_setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir


        self.bot.loop.create_task(self.setup_ticket_system())

    async def setup_ticket_system(self):
        print ("\n --> setup_ticket_system\n")
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(guild_id)


        was_created_list = []


# Creates a new Role
        role_name = "💼-support-team"
        role_colour = discord.Color.blue()
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
        role_colour = discord.Color.blue()
        aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
        aktiv_support_team_role = discord.utils.get(guild.roles, id=aktiv_support_team_role_id)

        if aktiv_support_team_role != None:
            print(f"The role {aktiv_support_team_role.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            aktiv_support_team_role = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {aktiv_support_team_role.name} was created.")
            write_config(config_dir, "role", "aktiv_support_team_role_id", aktiv_support_team_role.id)


# Creates a new Role
        role_name = "💼-aktiv-dm-support"
        role_colour = discord.Color.blue()
        aktiv_dm_support_id = read_config(config_dir,"role", "aktiv_dm_support_id", "int")
        aktiv_dm_support = discord.utils.get(guild.roles, id=aktiv_dm_support_id)

        if aktiv_dm_support != None:
            print(f"The role {aktiv_dm_support.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            aktiv_dm_support = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {aktiv_dm_support.name} was created.")
            write_config(config_dir, "role", "aktiv_dm_support_id", aktiv_dm_support.id)


# Creates a new category
        category_name = "------ 👮 - Support - 👮 ------"
        category_support_id = read_config(config_dir,"category", "category_support_id", "int")
        category_support = discord.utils.get(guild.categories, id=category_support_id)


        if category_support != None:
            print(f"The category {category_support.name} already exists.")

        else:
            print(f"The category {category_name} does not yet exist and will now be created")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),  # Everyone can view and join the channel
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
            description= """Please click the most relevant button to your issue below and answer the messages sent to you to the best of your ability.

**Please make sure your DMs are turned on as the bot will DM you your questions!**

> **🏆 VIP QUIZ 🏆**
> Use this ticket type to take part in the Vip Quiz.

> **🚨 Report Player 🚨**
> Use this ticket type to report a player for breaking the rules.

> **🔓 Ban Appeal 🔓**
> Use this ticket type to submit an unbanning request.

> **🐞 Bug Report 🐞**
> Use this ticket type to report a bug for our game server.

> **🌐 Support Ticket 🌐**
> If the other buttons are not applicable make a general support request.#
"""
            embed = discord.Embed(title="Hyper-Carry - Support System", description= description, colour=0x3498db)
            open_a_ticket_msg = await open_a_ticket_channel.send(embed=embed, view=ticket_button(self.bot))
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
                                colour=0x3498db)
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

    @discord.ui.button(label="Support check In", style=discord.ButtonStyle.green, custom_id="check_in")
    async def check_in(self, interaction: discord.Interaction, Button: discord.ui.Button):
        
        print(f"support_team_button [Support check In] --> get used by {interaction.user.name}")
        timestemp = time.time()
        discord_time_str = discord_time_convert(timestemp)
        aktiv_support_team_role_id = read_config(config_dir, "role", "aktiv_support_team_role_id", "int")
        support_team_role_id = read_config(config_dir, "role", "support_team_role_id", "int")
        support_team_channel_id = read_config(config_dir, "channel", "support_team_channel_id", "int")

        aktiv_support_team_role = interaction.guild.get_role(aktiv_support_team_role_id)
        support_team_role = interaction.guild.get_role(support_team_role_id)

        interaction_user_roles  = interaction.user.roles
        interaction_user_roles_id_list = []
        for id in interaction_user_roles:
            interaction_user_roles_id_list.append(id.id)


        if support_team_role.id not in interaction_user_roles_id_list:
            embed = discord.Embed(title=f"You are not in the @💼-support-team  \nask a admin to add your Support team role",
                        colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            if aktiv_support_team_role.id in interaction_user_roles_id_list:
                embed = discord.Embed(title=f"You are already checked in",
                            colour=0x3498db)
                await interaction.response.send_message(embed=embed, ephemeral=True)

            else:

                await interaction.response.defer(ephemeral=True)
                print(f"support_team_button [Support check In] --> get used by {interaction.user.name}")
                await interaction.user.add_roles(aktiv_support_team_role)

                support_entry_in_data(json_path_support, time.time(), interaction.user.name, interaction.user.id)

                description = f"""When a new ticket has opened, I will inform you here by pm.
                
                You can check out in the following channel:
                <#{support_team_channel_id}>
                
                **You are checked in** {discord_time_str}
                """
                embed = discord.Embed(title="💼 You have checked in as an  Aktiv-Support-Team 💼",
                            description=description,
                            colour=0x80ff80)
                await interaction.user.send(embed=embed)


                text = support_dashboard_text(json_path_ticket, interaction.guild.members, aktiv_support_team_role, support_team_role)
                embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                    description=text,
                                    colour=0x3498db)
                await interaction.message.edit(embed=embed)


    
    @discord.ui.button(label="Support check Out", style=discord.ButtonStyle.red, custom_id="check_out")
    async def check_out(self, interaction: discord.Interaction, Button: discord.ui.Button):

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
                
                text = support_dashboard_text(json_path_ticket, interaction.guild.members, aktiv_support_team_role, support_team_role)
                embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                    description=text,
                                    colour=0x3498db)
                await interaction.message.edit(embed=embed)

            else:
                embed = discord.Embed(title="💼 You are not checked in for now in to the active support team💼",
                      colour=0x3498db)
                await interaction.response.send_message(embed=embed, ephemeral=True)



# new button
class ticket_button(discord.ui.View, commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="🏆 VIP QUIZ 🏆", style=discord.ButtonStyle.green, custom_id="vip_quiz")
    async def vip_quiz_bot(self, interaction: discord.Interaction, button: discord.ui.Button):
        thumbnail = "https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png"

        user = interaction.user
        user_id = interaction.user.id
        data = read_json_file(json_path_ticket)
        ticket_action_id = new_ticket_action_id(ticket_aktion_id_dir)
        print(f"ticket_action_id = {ticket_action_id}")

        
        guild_id = read_config(config_dir,"client", "guild_id", "int")
        guild = self.bot.get_guild(guild_id)
        user = await guild.fetch_member(interaction.user.id)
        key = find_key_by_user_id(data, user_id)

        if key is not None and key is not False:
            ticket_status = data[key]["ticket_status"]
            ticket_channel_id = data[key]["ticket_channel_id"]
            unix_timestemp = data[key]["unix_timestemp"]
            discord_time = discord_time_convert(unix_timestemp)
            embed = discord.Embed(title="You already have a ticket or ticket PM open",
                    description=f"<#{ticket_channel_id}> {discord_time}",
                    colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))
            return
        

        ticket_channel_id_if_dm_support = get_ticket_channel_id_if_dm_support(json_path_ticket, user_id)

        if  ticket_channel_id_if_dm_support:
            key = find_key_by_user_id(data, user_id)
            data = read_json_file(json_path_ticket)
            unix_timestemp = data[key]["unix_timestemp"]
            discord_time = discord_time_convert(unix_timestemp)
            embed = discord.Embed(title=f"You already have a current ticket request.",
            description=f"Look into the /dm with <#{ticket_channel_id_if_dm_support}> {discord_time}",
            colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))
            return
        else:
            aktiv_dm_support_id = read_config(config_dir,"role", "aktiv_dm_support_id", "int")
            aktiv_dm_support = discord.utils.get(interaction.guild.roles, id=aktiv_dm_support_id)
            await interaction.user.add_roles(aktiv_dm_support)

            embed = discord.Embed(title="🏆 VIP QUIZ 🏆",
                                description="We are delighted that you would like to take part in the quiz.\nWe are keeping our fingers crossed for you.\nA quizmaster from our team will personally ask you the questions in your ticket channel.\n**GOOD LUCK!**\n\n > 🚫 Cancel 🚫\n> Cancel the ticket request.",
                                colour=0x00f406)

            embed.set_image(url="https://i.imgur.com/wlS5bJ7.jpeg")
            pm_start_msg = await interaction.user.send(embed=embed, view=cancel_dm_button(self.bot))
            content = f"***Your ticket has been successfully opened in our DMs***\n***Please answer the question from <#{pm_start_msg.channel.id}> that he sent to you.***"
            await interaction.response.send_message(content=content, embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))

            unix_timestemp = time.time()
            ticket_num = len(data)+2
            add_new_ticket_data(
                json_path=json_path_ticket,
                key = ticket_num,
                type = "vip quiz",
                user_name = user.name,
                user_id = user.id,
                ticket_channel_id = pm_start_msg.channel.id,
                ticket_role_id = "",
                time_stemp = unix_timestemp,
                ticket_action_id = ticket_action_id,
                ticket_status = "dm-queue")

            answers = []
            questions = [
            "Please provide your Steam64 ID"
            ]

            for question in questions:
                data = read_json_file(json_path_ticket)
                key = find_key_by_user_id(data, user_id)
                ticket_action_id_load = data[key]["ticket_action_id"]
                if ticket_action_id_load != ticket_action_id:
                    return
                embed = discord.Embed(title=f"{question}", colour=0x80ffff)
                await interaction.user.send(embed=embed)

                def check(m):
                    return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)

                try:
                    # Wait for user's response for up to 10 minutes
                    response = await interaction.client.wait_for('message', check=check, timeout=600)
                    answers.append(response.content)
                except asyncio.TimeoutError:
                    data = read_json_file(json_path_ticket)
                    key = find_key_by_user_id(data, user_id)
                    ticket_action_id_load = data[key]["ticket_action_id"]
                    if ticket_action_id_load != ticket_action_id:
                        return
                    open_a_ticket_channel_id = read_config(config_dir,"channel", "open_a_ticket_channel_id", "int")
                    text = f""" we assume the problem is resolved.
                                        We've closed your ticket. If the issue persists,
                                        feel free to open a new ticket in the channel
                                        <#{open_a_ticket_channel_id}>
                                        And we'll be happy to help."""
                    embed = discord.Embed(title=f"Since we didn't hear back from you," ,description =text, colour=0xf40006)
                    await interaction.user.send(embed=embed)
                    return
            
            data = read_json_file(json_path_ticket)
            key = find_key_by_user_id(data, user_id)
            ticket_action_id_load = data[key]["ticket_action_id"]
            if ticket_action_id_load != ticket_action_id:
                return

            user = await interaction.guild.fetch_member(interaction.user.id)
            # user_name = interaction.user.name
            user_name = interaction.user.name
            user_id = interaction.user.id
            unix_timestemp = time.time()
            ticket_status = "open"

            channel_name = f"📝-{user_name}-ticket-{ticket_num}"
            category_support_id = read_config(config_dir,"category", "category_support_id", "int")
            category_support = discord.utils.get(guild.categories, id=category_support_id)

            guild = interaction.client.get_guild(guild_id)
            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")

            guild = interaction.client.get_guild(guild_id)
            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")

            support_team_role = guild.get_role(support_team_role_id)

            role_colour = discord.Color.from_rgb(255, 255, 255)
            ticket = await interaction.guild.create_text_channel(channel_name, category=category_support)
            ticket_role = await guild.create_role(name=ticket.name, colour=role_colour)
            #ticket_role = discord.utils.get(interaction.guild.roles, name=interaction.channel.name)
            await interaction.user.add_roles(ticket_role)

            embed = discord.Embed(title="Ticket Dashboard",
                    description="The ticket can be managed here.\n\n**Except for Close, the buttons can only be used by the Support Team.**\n\n> **🔒 Close 🔒**\n> The ticket will be closed and will be archived.\n\n> **🛡️ Claim 🛡️**\n> Only for the support team to claim the ticket for processing.\n\n> **🎧 Need Voice 🎧**\n> A voice channel is created when one is needed for support.",
                    colour=0x00b0f4)
            ticket_dashboard = await ticket.send(embed=embed, view=claim_button())

            await ticket.set_permissions(guild.default_role, read_messages=False)
            await ticket.set_permissions(ticket_role, send_messages=True, read_messages=True)
            await ticket.set_permissions(support_team_role, send_messages=False, read_messages=True,)
            
            update_ticket_json_values(
                json_path_ticket,
                str(ticket_num),
                ticket.id,
                ticket_role.id,
                ticket_status)

            print(f"The channel {ticket.name} was created.")
            
            question_protocol_text = ""
            for i, (question, answer) in enumerate(zip(questions, answers)):
                question_protocol_text += f"**{question}**\n> {answer}\n\n"

            embed = discord.Embed(title="Question protocol -",
                    description=f"{question_protocol_text}",
                    colour=0x80ffff)
            embed.set_author(name="🏆 VIP QUIZ 🏆")
            
            ticket_dashboard = await ticket.send(embed=embed)

            
            confirmation_message = "🌟 Thank you for providing the information 🌟"
            text = f"""Your Quiz Host Master will get back to you in your ticket. GOOD LUCK!
            
            <#{ticket.id}>"""
            embed = discord.Embed(title=f"{confirmation_message}", description=f"{text}", colour=0x0080ff)
            embed.set_author(name="🏆 VIP QUIZ 🏆")
            await interaction.user.send(embed=embed)

            support_team_channel_id = read_config(config_dir,"channel", "support_team_channel_id", "int")
            support_team_msg_id = read_config(config_dir,"msg", "support_team_msg_id", "int")
            
            support_team_channel = guild.get_channel(support_team_channel_id)
            support_team_msg = await support_team_channel.fetch_message(support_team_msg_id)

            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")
            support_team_role = discord.utils.get(interaction.guild.roles, id=support_team_role_id)
            aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
            aktiv_support_team_role = discord.utils.get(interaction.guild.roles, id=aktiv_support_team_role_id)
            
            text = support_dashboard_text(json_path_ticket, interaction.guild.members, aktiv_support_team_role, support_team_role)
            embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                description=text,
                                colour=0x3498db)
            await support_team_msg.edit(embed=embed)

            aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
            # aktiv_support_team_role = guild.get_role(aktiv_support_team_role_id)
            discord_time = discord_time_convert(time.time())
            description=f"<#{ticket.id}>\nType: 🏆 VIP QUIZ 🏆\nfrom: <@{user_id}>\nopen: {discord_time}\n\n <#{support_team_channel}>"
            embed = discord.Embed(title="NEW OPEN Quiz Ticket", 
                    description=description,
                    colour=0x80ffff)

            aktiv_dm_support_id = read_config(config_dir,"role", "aktiv_dm_support_id", "int")
            aktiv_dm_support = discord.utils.get(interaction.guild.roles, id=aktiv_dm_support_id)
            await interaction.user.remove_roles(aktiv_dm_support)

            for aktive_member_role in aktiv_support_team_role.members:
                await aktive_member_role.send(embed=embed)


    @discord.ui.button(label="🚨 Player Report 🚨", style=discord.ButtonStyle.danger, custom_id="report_player")
    async def report_player_bot(self, interaction: discord.Interaction, button: discord.ui.Button):
        thumbnail = "https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png"

        user = interaction.user
        user_id = interaction.user.id
        data = read_json_file(json_path_ticket)
        ticket_action_id = new_ticket_action_id(ticket_aktion_id_dir)
        print(f"ticket_action_id = {ticket_action_id}")
        type = "report player"
        
        guild_id = read_config(config_dir,"client", "guild_id", "int")
        guild = self.bot.get_guild(guild_id)
        user = await guild.fetch_member(interaction.user.id)
        key = find_key_by_user_id(data, user_id)

        if key is not None and key is not False:
            ticket_status = data[key]["ticket_status"]
            ticket_channel_id = data[key]["ticket_channel_id"]
            unix_timestemp = data[key]["unix_timestemp"]
            discord_time = discord_time_convert(unix_timestemp)
            embed = discord.Embed(title="You already have a ticket or ticket PM open",
                    description=f"<#{ticket_channel_id}> {discord_time}",
                    colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))
            return
        

        ticket_channel_id_if_dm_support = get_ticket_channel_id_if_dm_support(json_path_ticket, user_id)

        if  ticket_channel_id_if_dm_support:
            key = find_key_by_user_id(data, user_id)
            data = read_json_file(json_path_ticket)
            unix_timestemp = data[key]["unix_timestemp"]
            discord_time = discord_time_convert(unix_timestemp)
            embed = discord.Embed(title=f"You already have a current ticket request.",
            description=f"Look into the /dm with <#{ticket_channel_id_if_dm_support}> {discord_time}",
            colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))
            return
        else:
            aktiv_dm_support_id = read_config(config_dir,"role", "aktiv_dm_support_id", "int")
            aktiv_dm_support = discord.utils.get(interaction.guild.roles, id=aktiv_dm_support_id)
            await interaction.user.add_roles(aktiv_dm_support)

            text_d = """We are grateful that you are reporting a player\n\n > 🚫 Cancel 🚫\n> Cancel the ticket request."""
            embed = discord.Embed(title="🚨 Player Report 🚨",
                                description=text_d,
                                colour=0x00f406)

            embed.set_thumbnail(url=thumbnail)
            pm_start_msg = await interaction.user.send(embed=embed, view=cancel_dm_button(self.bot))
            content = f"***Your ticket has been successfully opened in our DMs***\n***Please answer the question from <#{pm_start_msg.channel.id}> that he sent to you.***"
            await interaction.response.send_message(content=content, embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))

            unix_timestemp = time.time()
            ticket_num = len(data)+2
            add_new_ticket_data(
                json_path=json_path_ticket,
                key = ticket_num,
                type = "report player",
                user_name = user.name,
                user_id = user.id,
                ticket_channel_id = pm_start_msg.channel.id,
                ticket_role_id = "",
                time_stemp = unix_timestemp,
                ticket_action_id = ticket_action_id,
                ticket_status = "dm-queue")

            answers = []
            questions = [
            "(1/6) | What is the name of the player you are reporting, or do you have a link to their Steam profile?",
            "(2/6) | Please provide your Steam name or Steam profile link.",
            "(3/6) | Which server do you want to report the player on?",
            "(4/6) | What specific actions or behavior are you reporting the player for? Please provide details.",
            "(5/6) | Do you have any evidence to support your report, such as video recordings, demo, screenshots, or other documentation?",
            "(6/6) | Is there any additional information you would like to share before our team investigates the matter?"
            ]

            for question in questions:
                data = read_json_file(json_path_ticket)
                key = find_key_by_user_id(data, user_id)
                ticket_action_id_load = data[key]["ticket_action_id"]
                if ticket_action_id_load != ticket_action_id:
                    return
                embed = discord.Embed(title=f"{question}", colour=0x80ffff)
                await interaction.user.send(embed=embed)

                def check(m):
                    return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)

                try:
                    # Wait for user's response for up to 10 minutes
                    response = await interaction.client.wait_for('message', check=check, timeout=600)
                    answers.append(response.content)
                except asyncio.TimeoutError:
                    data = read_json_file(json_path_ticket)
                    key = find_key_by_user_id(data, user_id)
                    ticket_action_id_load = data[key]["ticket_action_id"]
                    if ticket_action_id_load != ticket_action_id:
                        return
                    open_a_ticket_channel_id = read_config(config_dir,"channel", "open_a_ticket_channel_id", "int")
                    text = f""" we assume the problem is resolved.
                                        We've closed your ticket. If the issue persists,
                                        feel free to open a new ticket in the channel
                                        <#{open_a_ticket_channel_id}>
                                        And we'll be happy to help."""
                    embed = discord.Embed(title=f"Since we didn't hear back from you," ,description =text, colour=0xf40006)
                    await interaction.user.send(embed=embed)
                    return
            
            data = read_json_file(json_path_ticket)
            key = find_key_by_user_id(data, user_id)
            ticket_action_id_load = data[key]["ticket_action_id"]
            if ticket_action_id_load != ticket_action_id:
                return

            user = await interaction.guild.fetch_member(interaction.user.id)
            # user_name = interaction.user.name
            user_name = interaction.user.name
            user_id = interaction.user.id
            unix_timestemp = time.time()
            ticket_status = "open"

            channel_name = f"📝-{user_name}-ticket-{ticket_num}"
            category_support_id = read_config(config_dir,"category", "category_support_id", "int")
            category_support = discord.utils.get(guild.categories, id=category_support_id)

            guild = interaction.client.get_guild(guild_id)
            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")

            guild = interaction.client.get_guild(guild_id)
            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")

            support_team_role = guild.get_role(support_team_role_id)

            role_colour = discord.Color.from_rgb(255, 255, 255)
            ticket = await interaction.guild.create_text_channel(channel_name, category=category_support)
            ticket_role = await guild.create_role(name=ticket.name, colour=role_colour)
            #ticket_role = discord.utils.get(interaction.guild.roles, name=interaction.channel.name)
            await interaction.user.add_roles(ticket_role)

            embed = discord.Embed(title="Ticket Dashboard",
                    description="The ticket can be managed here.\n\n**Except for Close, the buttons can only be used by the Support Team.**\n\n> **🔒 Close 🔒**\n> The ticket will be closed and will be archived.\n\n> **🛡️ Claim 🛡️**\n> Only for the support team to claim the ticket for processing.\n\n> **🎧 Need Voice 🎧**\n> A voice channel is created when one is needed for support.",
                    colour=0x00b0f4)
            ticket_dashboard = await ticket.send(embed=embed, view=claim_button())

            await ticket.set_permissions(guild.default_role, read_messages=False)
            await ticket.set_permissions(ticket_role, send_messages=True, read_messages=True)
            await ticket.set_permissions(support_team_role, send_messages=False, read_messages=True,)
            
            update_ticket_json_values(
                json_path_ticket,
                str(ticket_num),
                ticket.id,
                ticket_role.id,
                ticket_status)

            print(f"The channel {ticket.name} was created.")
            
            question_protocol_text = ""
            for i, (question, answer) in enumerate(zip(questions, answers)):
                question_protocol_text += f"**{question}**\n> {answer}\n\n"

            embed = discord.Embed(title="Question protocol -",
                    description=f"{question_protocol_text}",
                    colour=0x80ffff)
            embed.set_author(name="🚨 Player Report 🚨")
            
            ticket_dashboard = await ticket.send(embed=embed)

            
            confirmation_message = f"Your report has been submitted for review."
            text = f"""Our team will investigate the matter and take appropriate action.
            A ticket channel has been set up for you, where our support will take care of your request for you.
            
            <#{ticket.id}>"""
            embed = discord.Embed(title=f"{confirmation_message}", description=f"{text}", colour=0x0080ff)
            embed.set_author(name="🚨 Player Report 🚨")
            await interaction.user.send(embed=embed)

            support_team_channel_id = read_config(config_dir,"channel", "support_team_channel_id", "int")
            support_team_msg_id = read_config(config_dir,"msg", "support_team_msg_id", "int")
            
            support_team_channel = guild.get_channel(support_team_channel_id)
            support_team_msg = await support_team_channel.fetch_message(support_team_msg_id)

            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")
            support_team_role = discord.utils.get(interaction.guild.roles, id=support_team_role_id)
            aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
            aktiv_support_team_role = discord.utils.get(interaction.guild.roles, id=aktiv_support_team_role_id)
            
            text = support_dashboard_text(json_path_ticket, interaction.guild.members, aktiv_support_team_role, support_team_role)
            embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                description=text,
                                colour=0x3498db)
            await support_team_msg.edit(embed=embed)

            aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
            # aktiv_support_team_role = guild.get_role(aktiv_support_team_role_id)
            discord_time = discord_time_convert(time.time())
            description=f"<#{ticket.id}>\nType: 🚨 Player Report 🚨\nfrom: <@{user_id}>\nopen: {discord_time}\n\n <#{support_team_channel}>"
            embed = discord.Embed(title=f"NEW OPEN {type}", 
                    description=description,
                    colour=0x80ffff)

            aktiv_dm_support_id = read_config(config_dir,"role", "aktiv_dm_support_id", "int")
            aktiv_dm_support = discord.utils.get(interaction.guild.roles, id=aktiv_dm_support_id)
            await interaction.user.remove_roles(aktiv_dm_support)

            for aktive_member_role in aktiv_support_team_role.members:
                await aktive_member_role.send(embed=embed)

    

    @discord.ui.button(label="🔓 Ban Appeal 🔓", style=discord.ButtonStyle.green, custom_id="ban_appeal")
    async def ban_appeal_bot(self, interaction: discord.Interaction, button: discord.ui.Button):
        thumbnail = "https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png"

        user = interaction.user
        user_id = interaction.user.id
        data = read_json_file(json_path_ticket)
        ticket_action_id = new_ticket_action_id(ticket_aktion_id_dir)
        print(f"ticket_action_id = {ticket_action_id}")
        type = "ban appeal"
        
        guild_id = read_config(config_dir,"client", "guild_id", "int")
        guild = self.bot.get_guild(guild_id)
        user = await guild.fetch_member(interaction.user.id)
        key = find_key_by_user_id(data, user_id)

        if key is not None and key is not False:
            ticket_status = data[key]["ticket_status"]
            ticket_channel_id = data[key]["ticket_channel_id"]
            unix_timestemp = data[key]["unix_timestemp"]
            discord_time = discord_time_convert(unix_timestemp)
            embed = discord.Embed(title="You already have a ticket or ticket PM open",
                    description=f"<#{ticket_channel_id}> {discord_time}",
                    colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))
            return
        

        ticket_channel_id_if_dm_support = get_ticket_channel_id_if_dm_support(json_path_ticket, user_id)

        if  ticket_channel_id_if_dm_support:
            key = find_key_by_user_id(data, user_id)
            data = read_json_file(json_path_ticket)
            unix_timestemp = data[key]["unix_timestemp"]
            discord_time = discord_time_convert(unix_timestemp)
            embed = discord.Embed(title=f"You already have a current ticket request.",
            description=f"Look into the /dm with <#{ticket_channel_id_if_dm_support}> {discord_time}",
            colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))
            return
        else:
            aktiv_dm_support_id = read_config(config_dir,"role", "aktiv_dm_support_id", "int")
            aktiv_dm_support = discord.utils.get(interaction.guild.roles, id=aktiv_dm_support_id)
            await interaction.user.add_roles(aktiv_dm_support)

            text_d = """We hope that the ban was a misunderstanding and will try to help you.\n\n > 🚫 Cancel 🚫\n> Cancel the ticket request."""
            embed = discord.Embed(title="🔓 Ban Appeal 🔓",
                                description=text_d,
                                colour=0x00f406)

            embed.set_thumbnail(url=thumbnail)
            pm_start_msg = await interaction.user.send(embed=embed, view=cancel_dm_button(self.bot))
            content = f"***Your ticket has been successfully opened in our DMs***\n***Please answer the question from <#{pm_start_msg.channel.id}> that he sent to you.***"
            await interaction.response.send_message(content=content, embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))

            unix_timestemp = time.time()
            ticket_num = len(data)+2
            add_new_ticket_data(
                json_path=json_path_ticket,
                key = ticket_num,
                type = "ban appeal",
                user_name = user.name,
                user_id = user.id,
                ticket_channel_id = pm_start_msg.channel.id,
                ticket_role_id = "",
                time_stemp = unix_timestemp,
                ticket_action_id = ticket_action_id,
                ticket_status = "dm-queue")

            answers = []
            questions = [
            "(1/5) | What is your in-game username and Steam64 ID",
            "(2/5) | Which server or platform were you banned from?",
            "(3/5) | Can you provide the reason or context for your ban as you understand it?",
            "(4/5) | Have you learned from the incident that led to your ban, and what steps will you take to ensure it doesn't happen again?",
            "(5/5) | Is there any additional information you would like to share in support of your unban request? This could include evidence, an apology, or any other relevant details."
            ]

            for question in questions:
                data = read_json_file(json_path_ticket)
                key = find_key_by_user_id(data, user_id)
                ticket_action_id_load = data[key]["ticket_action_id"]
                if ticket_action_id_load != ticket_action_id:
                    return
                embed = discord.Embed(title=f"{question}", colour=0x80ffff)
                await interaction.user.send(embed=embed)

                def check(m):
                    return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)

                try:
                    # Wait for user's response for up to 10 minutes
                    response = await interaction.client.wait_for('message', check=check, timeout=600)
                    answers.append(response.content)
                except asyncio.TimeoutError:
                    data = read_json_file(json_path_ticket)
                    key = find_key_by_user_id(data, user_id)
                    ticket_action_id_load = data[key]["ticket_action_id"]
                    if ticket_action_id_load != ticket_action_id:
                        return
                    open_a_ticket_channel_id = read_config(config_dir,"channel", "open_a_ticket_channel_id", "int")
                    text = f""" we assume the problem is resolved.
                                        We've closed your ticket. If the issue persists,
                                        feel free to open a new ticket in the channel
                                        <#{open_a_ticket_channel_id}>
                                        And we'll be happy to help."""
                    embed = discord.Embed(title=f"Since we didn't hear back from you," ,description =text, colour=0xf40006)
                    await interaction.user.send(embed=embed)
                    return
            
            data = read_json_file(json_path_ticket)
            key = find_key_by_user_id(data, user_id)
            ticket_action_id_load = data[key]["ticket_action_id"]
            if ticket_action_id_load != ticket_action_id:
                return

            user = await interaction.guild.fetch_member(interaction.user.id)
            # user_name = interaction.user.name
            user_name = interaction.user.name
            user_id = interaction.user.id
            unix_timestemp = time.time()
            ticket_status = "open"

            channel_name = f"📝-{user_name}-ticket-{ticket_num}"
            category_support_id = read_config(config_dir,"category", "category_support_id", "int")
            category_support = discord.utils.get(guild.categories, id=category_support_id)

            guild = interaction.client.get_guild(guild_id)
            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")

            guild = interaction.client.get_guild(guild_id)
            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")

            support_team_role = guild.get_role(support_team_role_id)

            role_colour = discord.Color.from_rgb(255, 255, 255)
            ticket = await interaction.guild.create_text_channel(channel_name, category=category_support)
            ticket_role = await guild.create_role(name=ticket.name, colour=role_colour)
            #ticket_role = discord.utils.get(interaction.guild.roles, name=interaction.channel.name)
            await interaction.user.add_roles(ticket_role)

            embed = discord.Embed(title="Ticket Dashboard",
                    description="The ticket can be managed here.\n\n**Except for Close, the buttons can only be used by the Support Team.**\n\n> **🔒 Close 🔒**\n> The ticket will be closed and will be archived.\n\n> **🛡️ Claim 🛡️**\n> Only for the support team to claim the ticket for processing.\n\n> **🎧 Need Voice 🎧**\n> A voice channel is created when one is needed for support.",
                    colour=0x00b0f4)
            ticket_dashboard = await ticket.send(embed=embed, view=claim_button())

            await ticket.set_permissions(guild.default_role, read_messages=False)
            await ticket.set_permissions(ticket_role, send_messages=True, read_messages=True)
            await ticket.set_permissions(support_team_role, send_messages=False, read_messages=True,)
            
            update_ticket_json_values(
                json_path_ticket,
                str(ticket_num),
                ticket.id,
                ticket_role.id,
                ticket_status)

            print(f"The channel {ticket.name} was created.")
            
            question_protocol_text = ""
            for i, (question, answer) in enumerate(zip(questions, answers)):
                question_protocol_text += f"**{question}**\n> {answer}\n\n"

            embed = discord.Embed(title="Question protocol -",
                    description=f"{question_protocol_text}",
                    colour=0x80ffff)
            embed.set_author(name="🔓 Ban Appeal 🔓")
            
            ticket_dashboard = await ticket.send(embed=embed)

            
            confirmation_message = f"Your report has been submitted for review."
            text = f"""Our team will investigate the matter and take appropriate action.
            A ticket channel has been set up for you, where our support will take care of your request for you.
            
            <#{ticket.id}>"""
            embed = discord.Embed(title=f"{confirmation_message}", description=f"{text}", colour=0x0080ff)
            embed.set_author(name="🔓 Ban Appeal 🔓")
            await interaction.user.send(embed=embed)

            support_team_channel_id = read_config(config_dir,"channel", "support_team_channel_id", "int")
            support_team_msg_id = read_config(config_dir,"msg", "support_team_msg_id", "int")
            
            support_team_channel = guild.get_channel(support_team_channel_id)
            support_team_msg = await support_team_channel.fetch_message(support_team_msg_id)

            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")
            support_team_role = discord.utils.get(interaction.guild.roles, id=support_team_role_id)
            aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
            aktiv_support_team_role = discord.utils.get(interaction.guild.roles, id=aktiv_support_team_role_id)
            
            text = support_dashboard_text(json_path_ticket, interaction.guild.members, aktiv_support_team_role, support_team_role)
            embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                description=text,
                                colour=0x3498db)
            await support_team_msg.edit(embed=embed)

            aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
            # aktiv_support_team_role = guild.get_role(aktiv_support_team_role_id)
            discord_time = discord_time_convert(time.time())
            description=f"<#{ticket.id}>\nType: 🔓 Ban Appeal 🔓\nfrom: <@{user_id}>\nopen: {discord_time}\n\n <#{support_team_channel}>"
            embed = discord.Embed(title=f"NEW OPEN {type}", 
                    description=description,
                    colour=0x80ffff)

            aktiv_dm_support_id = read_config(config_dir,"role", "aktiv_dm_support_id", "int")
            aktiv_dm_support = discord.utils.get(interaction.guild.roles, id=aktiv_dm_support_id)
            await interaction.user.remove_roles(aktiv_dm_support)

            for aktive_member_role in aktiv_support_team_role.members:
                await aktive_member_role.send(embed=embed)


    @discord.ui.button(label="🐞 Bug Report 🐞", style=discord.ButtonStyle.gray, custom_id="bug_report")
    async def bug_report_bot(self, interaction: discord.Interaction, button: discord.ui.Button):
        thumbnail = "https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png"

        user = interaction.user
        user_id = interaction.user.id
        data = read_json_file(json_path_ticket)
        ticket_action_id = new_ticket_action_id(ticket_aktion_id_dir)
        print(f"ticket_action_id = {ticket_action_id}")
        type = "bug report"
        
        guild_id = read_config(config_dir,"client", "guild_id", "int")
        guild = self.bot.get_guild(guild_id)
        user = await guild.fetch_member(interaction.user.id)
        key = find_key_by_user_id(data, user_id)

        if key is not None and key is not False:
            ticket_status = data[key]["ticket_status"]
            ticket_channel_id = data[key]["ticket_channel_id"]
            unix_timestemp = data[key]["unix_timestemp"]
            discord_time = discord_time_convert(unix_timestemp)
            embed = discord.Embed(title="You already have a ticket or ticket PM open",
                    description=f"<#{ticket_channel_id}> {discord_time}",
                    colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))
            return
        

        ticket_channel_id_if_dm_support = get_ticket_channel_id_if_dm_support(json_path_ticket, user_id)

        if  ticket_channel_id_if_dm_support:
            key = find_key_by_user_id(data, user_id)
            data = read_json_file(json_path_ticket)
            unix_timestemp = data[key]["unix_timestemp"]
            discord_time = discord_time_convert(unix_timestemp)
            embed = discord.Embed(title=f"You already have a current ticket request.",
            description=f"Look into the /dm with <#{ticket_channel_id_if_dm_support}> {discord_time}",
            colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))
            return
        else:
            aktiv_dm_support_id = read_config(config_dir,"role", "aktiv_dm_support_id", "int")
            aktiv_dm_support = discord.utils.get(interaction.guild.roles, id=aktiv_dm_support_id)
            await interaction.user.add_roles(aktiv_dm_support)

            text_d = "Thank you for reporting a bug.\n\n > 🚫 Cancel 🚫\n> Cancel the ticket request."
            embed = discord.Embed(title="🐞 Bug Report 🐞",
                                description=text_d,
                                colour=0x00f406)

            embed.set_thumbnail(url=thumbnail)
            pm_start_msg = await interaction.user.send(embed=embed, view=cancel_dm_button(self.bot))
            content = f"***Your ticket has been successfully opened in our DMs***\n***Please answer the question from <#{pm_start_msg.channel.id}> that he sent to you.***"
            await interaction.response.send_message(content=content, embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))

            unix_timestemp = time.time()
            ticket_num = len(data)+2
            add_new_ticket_data(
                json_path=json_path_ticket,
                key = ticket_num,
                type = "bug_report",
                user_name = user.name,
                user_id = user.id,
                ticket_channel_id = pm_start_msg.channel.id,
                ticket_role_id = "",
                time_stemp = unix_timestemp,
                ticket_action_id = ticket_action_id,
                ticket_status = "dm-queue")

            answers = []
            questions = [
            "(1/6) | What is the name of the game you are experiencing the bug with?",
            "(2/6) | On which server are you experiencing this bug?",
            "(3/6) | Please describe the bug in detail. What unexpected behavior are you encountering?",
            "(4/6) | Can you provide steps to reproduce the bug? The more detailed, the better.",
            "(5/6) | When did you first encounter this bug? Please provide a date and time if possible.",
            "(6/6) | Is there any additional information you would like to share about the bug? Any suggestions for fixing it? Attach any demos, recordings, or console logs if available."
            ]

            for question in questions:
                data = read_json_file(json_path_ticket)
                key = find_key_by_user_id(data, user_id)
                ticket_action_id_load = data[key]["ticket_action_id"]
                if ticket_action_id_load != ticket_action_id:
                    return
                embed = discord.Embed(title=f"{question}", colour=0x80ffff)
                await interaction.user.send(embed=embed)

                def check(m):
                    return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)

                try:
                    # Wait for user's response for up to 10 minutes
                    response = await interaction.client.wait_for('message', check=check, timeout=600)
                    answers.append(response.content)
                except asyncio.TimeoutError:
                    data = read_json_file(json_path_ticket)
                    key = find_key_by_user_id(data, user_id)
                    ticket_action_id_load = data[key]["ticket_action_id"]
                    if ticket_action_id_load != ticket_action_id:
                        return
                    open_a_ticket_channel_id = read_config(config_dir,"channel", "open_a_ticket_channel_id", "int")
                    text = f""" we assume the problem is resolved.
                                        We've closed your ticket. If the issue persists,
                                        feel free to open a new ticket in the channel
                                        <#{open_a_ticket_channel_id}>
                                        And we'll be happy to help."""
                    embed = discord.Embed(title=f"Since we didn't hear back from you," ,description =text, colour=0xf40006)
                    await interaction.user.send(embed=embed)
                    return
            
            data = read_json_file(json_path_ticket)
            key = find_key_by_user_id(data, user_id)
            ticket_action_id_load = data[key]["ticket_action_id"]
            if ticket_action_id_load != ticket_action_id:
                return

            user = await interaction.guild.fetch_member(interaction.user.id)
            # user_name = interaction.user.name
            user_name = interaction.user.name
            user_id = interaction.user.id
            unix_timestemp = time.time()
            ticket_status = "open"

            channel_name = f"📝-{user_name}-ticket-{ticket_num}"
            category_support_id = read_config(config_dir,"category", "category_support_id", "int")
            category_support = discord.utils.get(guild.categories, id=category_support_id)

            guild = interaction.client.get_guild(guild_id)
            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")

            guild = interaction.client.get_guild(guild_id)
            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")

            support_team_role = guild.get_role(support_team_role_id)

            role_colour = discord.Color.from_rgb(255, 255, 255)
            ticket = await interaction.guild.create_text_channel(channel_name, category=category_support)
            ticket_role = await guild.create_role(name=ticket.name, colour=role_colour)
            #ticket_role = discord.utils.get(interaction.guild.roles, name=interaction.channel.name)
            await interaction.user.add_roles(ticket_role)

            embed = discord.Embed(title="Ticket Dashboard",
                    description="The ticket can be managed here.\n\n**Except for Close, the buttons can only be used by the Support Team.**\n\n> **🔒 Close 🔒**\n> The ticket will be closed and will be archived.\n\n> **🛡️ Claim 🛡️**\n> Only for the support team to claim the ticket for processing.\n\n> **🎧 Need Voice 🎧**\n> A voice channel is created when one is needed for support.",
                    colour=0x00b0f4)
            ticket_dashboard = await ticket.send(embed=embed, view=claim_button())

            await ticket.set_permissions(guild.default_role, read_messages=False)
            await ticket.set_permissions(ticket_role, send_messages=True, read_messages=True)
            await ticket.set_permissions(support_team_role, send_messages=False, read_messages=True,)
            
            update_ticket_json_values(
                json_path_ticket,
                str(ticket_num),
                ticket.id,
                ticket_role.id,
                ticket_status)

            print(f"The channel {ticket.name} was created.")
            
            question_protocol_text = ""
            for i, (question, answer) in enumerate(zip(questions, answers)):
                question_protocol_text += f"**{question}**\n> {answer}\n\n"

            embed = discord.Embed(title="Question protocol -",
                    description=f"{question_protocol_text}",
                    colour=0x80ffff)
            embed.set_author(name="🐞 Bug Report 🐞")
            
            ticket_dashboard = await ticket.send(embed=embed)

            
            confirmation_message = f"Your report has been submitted for review."
            text = f"""Our team will investigate the matter and take appropriate action.
            A ticket channel has been set up for you, where our support will take care of your request for you.
            
            <#{ticket.id}>"""
            embed = discord.Embed(title=f"{confirmation_message}", description=f"{text}", colour=0x0080ff)
            embed.set_author(name="🐞 Bug Report 🐞")
            await interaction.user.send(embed=embed)

            support_team_channel_id = read_config(config_dir,"channel", "support_team_channel_id", "int")
            support_team_msg_id = read_config(config_dir,"msg", "support_team_msg_id", "int")
            
            support_team_channel = guild.get_channel(support_team_channel_id)
            support_team_msg = await support_team_channel.fetch_message(support_team_msg_id)

            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")
            support_team_role = discord.utils.get(interaction.guild.roles, id=support_team_role_id)
            aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
            aktiv_support_team_role = discord.utils.get(interaction.guild.roles, id=aktiv_support_team_role_id)
            
            text = support_dashboard_text(json_path_ticket, interaction.guild.members, aktiv_support_team_role, support_team_role)
            embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                description=text,
                                colour=0x3498db)
            await support_team_msg.edit(embed=embed)

            aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
            # aktiv_support_team_role = guild.get_role(aktiv_support_team_role_id)
            discord_time = discord_time_convert(time.time())
            description=f"<#{ticket.id}>\nType: 🐞 Bug Report 🐞\nfrom: <@{user_id}>\nopen: {discord_time}\n\n <#{support_team_channel}>"
            embed = discord.Embed(title=f"NEW OPEN {type}", 
                    description=description,
                    colour=0x80ffff)

            aktiv_dm_support_id = read_config(config_dir,"role", "aktiv_dm_support_id", "int")
            aktiv_dm_support = discord.utils.get(interaction.guild.roles, id=aktiv_dm_support_id)
            await interaction.user.remove_roles(aktiv_dm_support)

            for aktive_member_role in aktiv_support_team_role.members:
                await aktive_member_role.send(embed=embed)



    @discord.ui.button(label="🌐 Support Ticket 🌐", style=discord.ButtonStyle.primary, custom_id="general_ticket")
    async def general_ticket_bot(self, interaction: discord.Interaction, button: discord.ui.Button):
        thumbnail = "https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png"

        user = interaction.user
        user_id = interaction.user.id
        data = read_json_file(json_path_ticket)
        ticket_action_id = new_ticket_action_id(ticket_aktion_id_dir)
        print(f"ticket_action_id = {ticket_action_id}")
        type = "general ticket"
        
        guild_id = read_config(config_dir,"client", "guild_id", "int")
        guild = self.bot.get_guild(guild_id)
        user = await guild.fetch_member(interaction.user.id)
        key = find_key_by_user_id(data, user_id)

        if key is not None and key is not False:
            ticket_status = data[key]["ticket_status"]
            ticket_channel_id = data[key]["ticket_channel_id"]
            unix_timestemp = data[key]["unix_timestemp"]
            discord_time = discord_time_convert(unix_timestemp)
            embed = discord.Embed(title="You already have a ticket or ticket PM open",
                    description=f"<#{ticket_channel_id}> {discord_time}",
                    colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))
            return
        

        ticket_channel_id_if_dm_support = get_ticket_channel_id_if_dm_support(json_path_ticket, user_id)

        if  ticket_channel_id_if_dm_support:
            key = find_key_by_user_id(data, user_id)
            data = read_json_file(json_path_ticket)
            unix_timestemp = data[key]["unix_timestemp"]
            discord_time = discord_time_convert(unix_timestemp)
            embed = discord.Embed(title=f"You already have a current ticket request.",
            description=f"Look into the /dm with <#{ticket_channel_id_if_dm_support}> {discord_time}",
            colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))
            return
        else:
            aktiv_dm_support_id = read_config(config_dir,"role", "aktiv_dm_support_id", "int")
            aktiv_dm_support = discord.utils.get(interaction.guild.roles, id=aktiv_dm_support_id)
            await interaction.user.add_roles(aktiv_dm_support)

            text_d = "We hope to be able to help you quickly.\n\n > 🚫 Cancel 🚫\n> Cancel the ticket request."
            embed = discord.Embed(title="🌐 Support Ticket 🌐",
                                description=text_d,
                                colour=0x00f406)

            embed.set_thumbnail(url=thumbnail)
            pm_start_msg = await interaction.user.send(embed=embed, view=cancel_dm_button(self.bot))
            content = f"***Your ticket has been successfully opened in our DMs***\n***Please answer the question from <#{pm_start_msg.channel.id}> that he sent to you.***"
            await interaction.response.send_message(content=content, embed=embed, ephemeral=True, view=cancel_dm_button(self.bot))

            unix_timestemp = time.time()
            ticket_num = len(data)+2
            add_new_ticket_data(
                json_path=json_path_ticket,
                key = ticket_num,
                type = "general_ticket",
                user_name = user.name,
                user_id = user.id,
                ticket_channel_id = pm_start_msg.channel.id,
                ticket_role_id = "",
                time_stemp = unix_timestemp,
                ticket_action_id = ticket_action_id,
                ticket_status = "dm-queue")

            answers = []
            questions = [
            "(1/5) | What is the nature of the issue or question you need support with?",
            "(2/5) | Please provide any relevant details or context about the issue.",
            "(3/5) | Which platform or service is the issue related to?",
            "(4/5) | Have you attempted any troubleshooting steps? If yes, please describe them.",
            "(5/5) | Is there any additional information you would like to share or any specific assistance you are seeking?"
            ]

            for question in questions:
                data = read_json_file(json_path_ticket)
                key = find_key_by_user_id(data, user_id)
                ticket_action_id_load = data[key]["ticket_action_id"]
                if ticket_action_id_load != ticket_action_id:
                    return
                embed = discord.Embed(title=f"{question}", colour=0x80ffff)
                await interaction.user.send(embed=embed)

                def check(m):
                    return m.author == interaction.user and isinstance(m.channel, discord.DMChannel)

                try:
                    # Wait for user's response for up to 10 minutes
                    response = await interaction.client.wait_for('message', check=check, timeout=600)
                    answers.append(response.content)
                except asyncio.TimeoutError:
                    data = read_json_file(json_path_ticket)
                    key = find_key_by_user_id(data, user_id)
                    ticket_action_id_load = data[key]["ticket_action_id"]
                    if ticket_action_id_load != ticket_action_id:
                        return
                    open_a_ticket_channel_id = read_config(config_dir,"channel", "open_a_ticket_channel_id", "int")
                    text = f""" we assume the problem is resolved.
                                        We've closed your ticket. If the issue persists,
                                        feel free to open a new ticket in the channel
                                        <#{open_a_ticket_channel_id}>
                                        And we'll be happy to help."""
                    embed = discord.Embed(title=f"Since we didn't hear back from you," ,description =text, colour=0xf40006)
                    await interaction.user.send(embed=embed)
                    return
            
            data = read_json_file(json_path_ticket)
            key = find_key_by_user_id(data, user_id)
            ticket_action_id_load = data[key]["ticket_action_id"]
            if ticket_action_id_load != ticket_action_id:
                return

            user = await interaction.guild.fetch_member(interaction.user.id)
            # user_name = interaction.user.name
            user_name = interaction.user.name
            user_id = interaction.user.id
            unix_timestemp = time.time()
            ticket_status = "open"

            channel_name = f"📝-{user_name}-ticket-{ticket_num}"
            category_support_id = read_config(config_dir,"category", "category_support_id", "int")
            category_support = discord.utils.get(guild.categories, id=category_support_id)

            guild = interaction.client.get_guild(guild_id)
            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")

            guild = interaction.client.get_guild(guild_id)
            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")

            support_team_role = guild.get_role(support_team_role_id)

            role_colour = discord.Color.from_rgb(255, 255, 255)
            ticket = await interaction.guild.create_text_channel(channel_name, category=category_support)
            ticket_role = await guild.create_role(name=ticket.name, colour=role_colour)
            #ticket_role = discord.utils.get(interaction.guild.roles, name=interaction.channel.name)
            await interaction.user.add_roles(ticket_role)

            embed = discord.Embed(title="Ticket Dashboard",
                    description="The ticket can be managed here.\n\n**Except for Close, the buttons can only be used by the Support Team.**\n\n> **🔒 Close 🔒**\n> The ticket will be closed and will be archived.\n\n> **🛡️ Claim 🛡️**\n> Only for the support team to claim the ticket for processing.\n\n> **🎧 Need Voice 🎧**\n> A voice channel is created when one is needed for support.",
                    colour=0x00b0f4)
            ticket_dashboard = await ticket.send(embed=embed, view=claim_button())

            await ticket.set_permissions(guild.default_role, read_messages=False)
            await ticket.set_permissions(ticket_role, send_messages=True, read_messages=True)
            await ticket.set_permissions(support_team_role, send_messages=False, read_messages=True,)
            
            update_ticket_json_values(
                json_path_ticket,
                str(ticket_num),
                ticket.id,
                ticket_role.id,
                ticket_status)

            print(f"The channel {ticket.name} was created.")
            
            question_protocol_text = ""
            for i, (question, answer) in enumerate(zip(questions, answers)):
                question_protocol_text += f"**{question}**\n> {answer}\n\n"

            embed = discord.Embed(title="Question protocol -",
                    description=f"{question_protocol_text}",
                    colour=0x80ffff)
            embed.set_author(name="🌐 Support Ticket 🌐")
            
            ticket_dashboard = await ticket.send(embed=embed)

            
            confirmation_message = f"Your report has been submitted for review."
            text = f"""Our team will investigate the matter and take appropriate action.
            A ticket channel has been set up for you, where our support will take care of your request for you.
            
            <#{ticket.id}>"""
            embed = discord.Embed(title=f"{confirmation_message}", description=f"{text}", colour=0x0080ff)
            embed.set_author(name="🌐 Support Ticket 🌐")
            await interaction.user.send(embed=embed)

            support_team_channel_id = read_config(config_dir,"channel", "support_team_channel_id", "int")
            support_team_msg_id = read_config(config_dir,"msg", "support_team_msg_id", "int")
            
            support_team_channel = guild.get_channel(support_team_channel_id)
            support_team_msg = await support_team_channel.fetch_message(support_team_msg_id)

            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")
            support_team_role = discord.utils.get(interaction.guild.roles, id=support_team_role_id)
            aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
            aktiv_support_team_role = discord.utils.get(interaction.guild.roles, id=aktiv_support_team_role_id)
            
            text = support_dashboard_text(json_path_ticket, interaction.guild.members, aktiv_support_team_role, support_team_role)
            embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                description=text,
                                colour=0x3498db)
            await support_team_msg.edit(embed=embed)

            aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
            # aktiv_support_team_role = guild.get_role(aktiv_support_team_role_id)
            discord_time = discord_time_convert(time.time())
            description=f"<#{ticket.id}>\nType: 🌐 Support Ticket 🌐\nfrom: <@{user_id}>\nopen: {discord_time}\n\n <#{support_team_channel}>"
            embed = discord.Embed(title=f"NEW OPEN {type}", 
                    description=description,
                    colour=0x80ffff)

            aktiv_dm_support_id = read_config(config_dir,"role", "aktiv_dm_support_id", "int")
            aktiv_dm_support = discord.utils.get(interaction.guild.roles, id=aktiv_dm_support_id)
            await interaction.user.remove_roles(aktiv_dm_support)

            for aktive_member_role in aktiv_support_team_role.members:
                await aktive_member_role.send(embed=embed)



class claim_button(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="🛡️ Claim 🛡️", style=discord.ButtonStyle.success , custom_id="claim")
    async def claim_ticket(self, interaction: discord.Interaction, Button: discord.ui.Button):
        thumbnail = "https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png"

        user = interaction.user
        user_id = interaction.user.id

        aktiv_support_team_role_id = read_config(config_dir, "role", "aktiv_support_team_role_id", "int")
        support_team_role_id = read_config(config_dir, "role", "support_team_role_id", "int")
        support_team_role = discord.utils.get(interaction.guild.roles, id=support_team_role_id)
        support_team_channel_id = read_config(config_dir, "channel", "support_team_channel_id", "int")
        support_team_channel =  discord.utils.get(interaction.guild.channels, id=support_team_channel_id)
        

        support_team_data = read_json_file(json_path_support)
        json_ticket = read_json_file(json_path_ticket)
        
        
        key = find_key_by_ticket_channel(json_ticket, interaction.channel.id)

        suport_claimed_list = find_user_ids_by_ticket(support_team_data, key)
        if interaction.user.id in suport_claimed_list:
                embed = discord.Embed(title="You have claimed the ticket already!",
                    colour=0xff80ff)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            support_team_msg_id = read_config(config_dir, "msg", "support_team_msg_id", "int")
            support_team_msg = await support_team_channel.fetch_message(support_team_msg_id)
        
            user = await interaction.guild.fetch_member(interaction.user.id)
            user_rols = user.roles
            role_list = []
            for role_id in user_rols:
                role_list.append(role_id.id)
                print(f"role_id = {role_id} = {type(role_id)}")

            if aktiv_support_team_role_id  not in role_list:
                
                if aktiv_support_team_role_id  not in role_list and support_team_role.id in role_list:
                    embed = discord.Embed(title=f"You can't claim the ticket.",
                            description=f"You are not in the <@&{aktiv_support_team_role_id}>\nGo Check in at\n<#{support_team_channel_id}>",
                            colour=0x3498db)
                    await interaction.response.send_message(embed=embed,ephemeral=True)
                else:
                    embed = discord.Embed(title="You don't have the rights to do that.",
                        description=f"You are not in the <@&{support_team_role_id}>",
                        colour=0x3498db)
                    await interaction.response.send_message(embed=embed,ephemeral=True)

            else:

                role_list = []
                for role in interaction.user.roles:
                    role_list.append(role.name)

                if interaction.channel.name in role_list:

                    embed = discord.Embed(title="You have already claimed the ticket",
                            colour=0x3498db)
                    await interaction.response.send_message(embed=embed,ephemeral=True)

                else:

                    embed = discord.Embed(title="You have claimed the ticket!",
                                colour=0xff80ff)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    

                    ticket_role = discord.utils.get(interaction.guild.roles, name=interaction.channel.name)
                    await interaction.user.add_roles(ticket_role)

                    json_support = read_json_file(json_path_support)
                    support_key = find_last_entry_key(json_support, interaction.user.id)
                    add_tickt_to_support_data(json_path_support, json_support, support_key, key)

                    update_json(json_path_ticket, str(key), "ticket_status", "claimed", loaded_data=json_ticket)


                    support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")
                    support_team_role = discord.utils.get(interaction.guild.roles, id=support_team_role_id)
                    aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
                    aktiv_support_team_role = discord.utils.get(interaction.guild.roles, id=aktiv_support_team_role_id)

                    # support_team_msg_id = read_config(config_dir, "msg", "support_team_msg_id", "int")
                    # support_team_channel_id = read_config(config_dir, "channel", "support_team_channel_id", "int")
                    # support_team_channel =  discord.utils.get(interaction.guild.channels, id=support_team_channel_id)
                    # support_team_msg = await support_team_channel.fetch_message(support_team_msg_id)

                    text = support_dashboard_text(json_path_ticket, interaction.guild.members, aktiv_support_team_role, support_team_role)
                    embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                        description=text,
                                        colour=0x3498db)
                    await support_team_msg.edit(embed=embed)



    @discord.ui.button(label="🎧 Need Voice 🎧", style=discord.ButtonStyle.primary , custom_id="need_voice")
    async def need_voice_support(self, interaction: discord.Interaction, Button: discord.ui.Button):
        thumbnail = "https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png"

        guild = interaction.guild
        user = interaction.user
        user_id = interaction.user.id
        support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")
        support_team_role = discord.utils.get(interaction.guild.roles, id=support_team_role_id)
        aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
        aktiv_support_team_role = discord.utils.get(interaction.guild.roles, id=aktiv_support_team_role_id)

        role_list = []
        for role in interaction.user.roles:
            role_list.append(role.name)

        if interaction.channel.name not in role_list:
            embed = discord.Embed(title="You do not have the rights to open Voice Support.",
                description=f"You must first claim the ticket.",
                colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        
        if  aktiv_support_team_role.name in role_list and interaction.channel.name in role_list:

            all_voice_channel_names = []
            all_voice_channels = interaction.guild.voice_channels
            for voice_c in all_voice_channels:
                all_voice_channel_names.append(voice_c.name)

            if interaction.channel.name not in all_voice_channel_names:

                category_support_id = read_config(config_dir, "category", "category_support_id", "int")
                category_support = discord.utils.get(interaction.guild.categories, id=category_support_id)


                ticket_role = discord.utils.get(interaction.guild.roles, name=interaction.channel.name)
                
                ticket_voice_channel = await interaction.guild.create_voice_channel(interaction.channel.name, category=category_support)
                await ticket_voice_channel.set_permissions(guild.default_role, read_messages=False)
                await ticket_voice_channel.set_permissions(ticket_role, send_messages=True, read_messages=True)

                json_ticket = read_json_file(json_path_ticket)
                key = find_key_by_ticket_channel(json_ticket, interaction.channel.id)
                user_id = json_ticket[key]["user_id"]
                ticket_user = await interaction.guild.fetch_member(user_id)

                embed = discord.Embed(title="🎧 New voice channel for your voice support 🎧",
                        description=f"Use the the voice channel to receive your **support over voice**\n\n<#{ticket_voice_channel.id}>",
                        colour=0xff80ff)
                await interaction.response.send_message(embed=embed)
                try:
                    await interaction.user.move_to(ticket_voice_channel)
                    await ticket_user.move_to(ticket_voice_channel)
                except:
                    pass
                await ticket_user.send(embed=embed)

                json_ticket = read_json_file(json_path_ticket)
                key = find_key_by_ticket_channel(json_ticket, interaction.channel.id)
                update_json(json_path_ticket, key, "voice_channel_id", ticket_voice_channel.id , loaded_data=json_ticket)
                update_json(json_path_ticket, key, "ticket_status", "voice-support", loaded_data=json_ticket)

                support_team_msg_id = read_config(config_dir, "msg", "support_team_msg_id", "int")
                support_team_channel_id = read_config(config_dir, "channel", "support_team_channel_id", "int")
                support_team_channel =  discord.utils.get(interaction.guild.channels, id=support_team_channel_id)
                support_team_msg = await support_team_channel.fetch_message(support_team_msg_id)

                text = support_dashboard_text(json_path_ticket, interaction.guild.members, aktiv_support_team_role, support_team_role)
                embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                    description=text,
                                    colour=0x3498db)
                await support_team_msg.edit(embed=embed)
            
            else:

                voice_support_channel = discord.utils.get(interaction.guild.voice_channels, name=interaction.channel.name)
                embed = discord.Embed(description=f"A voice channel already exists \n<#{voice_support_channel.id}>")
                await interaction.response.send_message(embed=embed, ephemeral=True)

            

        else:
            try:
                embed = discord.Embed(title="🎧 Support Voice chat can only be opened by the support team 🎧",
                        description=f"If you would like support via voice, ask to your supporter about it.",
                        colour=0xff80ff)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except:
                pass


    @discord.ui.button(label="🔒 Close 🔒", style=discord.ButtonStyle.danger , custom_id="close")
    async def close_ticket(self, interaction: discord.Interaction, Button: discord.ui.Button):
        thumbnail = "https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png"

        user = interaction.user
        user_id = interaction.user.id

        role_list = []
        for role in interaction.user.roles:
            role_list.append(role.name)


        if interaction.channel.name not in role_list:
            embed = discord.Embed(title="You do not have the right to close the ticket.",
                description=f"You must first claim the ticket to close it.",
                colour=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:

            discord_time = discord_time_convert(time.time())
            embed = discord.Embed(title="🔒 Ticket Closed 🔒",
                        description=f"The ticket was closed by <@{user_id}>.\n{discord_time}",
                        colour=0x00b0f4)
            await interaction.response.edit_message(embed=embed, view=None)

            json_ticket = read_json_file(json_path_ticket)
            key = find_key_by_ticket_channel(json_ticket, interaction.channel.id)
            
            ticket_role_id = json_ticket[key]["ticket_role_id"]
            ticket_role = discord.utils.get(interaction.guild.roles, id=ticket_role_id)
            

            voice_channel_id = json_ticket[key]["voice_channel_id"]
            voice_channel = interaction.guild.get_channel(voice_channel_id)

            if voice_channel != None:
                await voice_channel.delete()

            update_json(json_path_ticket, key, "ticket_status", "close")

            await ticket_role.delete()

            category_ticket_archiv_id = read_config(config_dir, "category", "category_ticket_archiv_id", "int")
            category_ticket_archiv = discord.utils.get(interaction.guild.categories, id=category_ticket_archiv_id)

            await interaction.channel.edit(category=category_ticket_archiv)

            # add Ticket msg save extern  <--
            support_team_role_id = read_config(config_dir,"role", "support_team_role_id", "int")
            support_team_role = discord.utils.get(interaction.guild.roles, id=support_team_role_id)
            aktiv_support_team_role_id = read_config(config_dir,"role", "aktiv_support_team_role_id", "int")
            aktiv_support_team_role = discord.utils.get(interaction.guild.roles, id=aktiv_support_team_role_id)

            support_team_msg_id = read_config(config_dir, "msg", "support_team_msg_id", "int")
            support_team_channel_id = read_config(config_dir, "channel", "support_team_channel_id", "int")
            support_team_channel =  discord.utils.get(interaction.guild.channels, id=support_team_channel_id)
            support_team_msg = await support_team_channel.fetch_message(support_team_msg_id)


            text = support_dashboard_text(json_path_ticket, interaction.guild.members, aktiv_support_team_role, support_team_role)
            embed = discord.Embed(title="💼 Support Team - Dashboard 💼",
                                description=text,
                                colour=0x3498db)
            await support_team_msg.edit(embed=embed)


class cancel_dm_button(discord.ui.View):
    def __init__(self, bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="🚫 Cancel 🚫", style=discord.ButtonStyle.danger, custom_id="cancel_dm_button")
    async def claim_ticket(self, interaction: discord.Interaction, Button: discord.ui.Button):
        thumbnail = "https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png"

        user = interaction.user
        user_id = interaction.user.id
        self.cancelled = True
        open_a_ticket_channel_id = read_config(config_dir, "channel", "open_a_ticket_channel_id", "int")
        aktiv_dm_support_id = read_config(config_dir, "role", "aktiv_dm_support_id", "int")

        guild = self.bot.get_guild(guild_id)
        user = await guild.fetch_member(interaction.user.id)
        delete_dm_tickets_data(json_path_ticket, user_id)

        aktiv_dm_support = discord.utils.get(guild.roles, id=aktiv_dm_support_id)
        await user.remove_roles(aktiv_dm_support)

        embed = discord.Embed(
            title="**The ticket has been channelled.**",
            description=f"You can open a new ticket if you like at:\n<#{open_a_ticket_channel_id}>",
            colour=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.user.send(embed=embed)
            



async def setup(bot: commands.Bot):
    await bot.add_cog(ticket_system_setup(bot), guild=discord.Object(guild_id))
    bot.add_view(ticket_button(bot))
    bot.add_view(support_team_button())
    bot.add_view(claim_button())
    bot.add_view(cancel_dm_button(bot))


"""     
print("\n")
print( "= {} = {}")
print("\n")
        
        """