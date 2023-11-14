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


# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")
category_private_voice_id = int(read_config(config_dir, "category", "category_private_voice_id"))
json_path = os.path.join(current_dir, "channel_data.json")




guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1


create_channel_id =  read_config(config_dir, "channel", "create_channel_id", "int")

if create_channel_id == None:
    create_channel_id = 1

category_private_voice_id = read_config(config_dir, "category", "category_private_voice_id", "int")
if category_private_voice_id == None:
    category_private_voice_id = 1


class TicketCog(commands.Cog):
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

# Creates a new category
        category_name = "------ 👮 - Support - 👮 ------"
        category_support = discord.utils.get(guild.categories, name=category_name)

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
            write_config(config_dir, "channel","category_support_id", category_support_id)

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


            open_a_ticket_msg_id = read_config(config_dir,"msg", "open_a_ticket_msg_id", "int")
            try:
                open_a_ticket_msg = await open_a_ticket_channel.fetch_message(open_a_ticket_msg_id)
                print(f"The channel open_a_ticket_msg already exists.")
                
            except:
                embed = discord.Embed(title="Space holder for Ticket msg", description="The ticket system window", color=0x00ff00)
                open_a_ticket_msg = await open_a_ticket_channel.send(embed=embed)
                write_config(config_dir, "msg", "open_a_ticket_msg_id", open_a_ticket_msg.id)


# Creates a new category
        category_name = "-----📚-ticket-archiv-📚-----"
        category_ticket_archiv = discord.utils.get(guild.categories, name=category_name)

        if category_ticket_archiv != None:
            print(f"The category {category_ticket_archiv.name} already exists.")

        else:
            print(f"The category {category_name} does not yet exist and will now be created")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }
        
            category_ticket_archiv = await guild.create_category(category_name, overwrites=overwrites)
            print(f"The category {category_name} was created.")
            category_ticket_archiv_id = category_ticket_archiv.id
            write_config(config_dir, "channel","category_ticket_archiv_id", category_ticket_archiv_id)

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





async def setup(bot: commands.Bot):
    await bot.add_cog(TicketCog(bot), guild=discord.Object(guild_id))





"""#player_have_channel_list = []
class bot_ticket_system(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_channels = {}  # A dictionary for tracking the channels created <-- bug if restart forgott old channels
        #self.player_have_channel_list = {}
    async def create_voice_channel(self, user):
        category = discord.utils.get(user.guild.categories, id=category_private_voice_id)



class ticket_button(discord.ui.View,):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="🚨 Report Player 🚨", style=discord.ButtonStyle.red, custom_id="report")
    async def report_player(self, interaction: discord.Interaction, Button: discord.ui.Button):
        thumbnail = "https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png"
        
        user = interaction.user
        user_id = interaction.user.id

        user.send()
        text_1 = "Thank you for using our reporting system! To expedite the resolution process, we kindly request you to answer six essential questions before our team addresses your report. If you change your mind, you can cancel the report with !stop, or it will automatically expire after 10 minutes without a response."
        embed = discord.Embed(title="🚨 Report Player 🚨",
                      description=text_1,
                      colour=0xf40006)
        embed.set_author(name="👮 Your personal support agent👮")
        embed.set_thumbnail(url=thumbnail)



        text_2 = "What is the name of the player you are reporting, or do you have a link to their Steam profile?"
        text_3 = "Please provide your Steam name or Steam profile link."
        text_4 = "Which server do you want to report the player on?"
        text_5 = "What specific actions or behavior are you reporting the player for? Please provide details."
        text_6 = "Do you have any evidence to support your report, such as video recordings, demo, screenshots, or other documentation?"
        text_7 = "Is there any additional information you would like to share before our team investigates the matter?"




async def setup(bot: commands.Bot):
    # await bot.add_cog(bot_ticket_system(bot), guild=discord.Object(guild_id))
    bot.add_view(ticket_button())"""