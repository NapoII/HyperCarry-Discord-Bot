"""Full Doku on: https://github.com/NapoII/HyperCarry-Disocrd-Bot"
-----------------------------------------------
!!! ADD MUST HAVE INFO !!

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

        # "Work_Folder.Rust.test"
        # "discord_cogs.admin.say",
        self.initial_extensions = [
            "discord_cogs.ticket_system.ticket_system",
            "discord_cogs.channel_hopper.channel_hopper",
        ]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild=discord.Object(guild_id))

    async def on_ready(self, ):
        print("Discord Bot prints in | wait_until_ready")
        await self.wait_until_ready()
        print(f'printged in as {self.user} (ID: {self.user.id})')

        await self.wait_until_ready()  
        guild = self.get_guild(guild_id) 

        was_created_list = []


# Creates a new category
        category_name = "--------💻 - Admin - 💻--------"
        category_adminl_id = read_config(config_dir,"channel", "open_a_ticket_channel_id", "int")
        category_admin = discord.utils.get(guild.text_channels, id=category_adminl_id)

        if category_admin != None:
            print(f"The category {category_admin.name} already exists.")

        else:
            print(f"The category {category_name} does not yet exist and will now be created")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }
        
            category_admin = await guild.create_category(category_name, overwrites=overwrites)
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
            bot_cmd_channel = await guild.create_text_channel(bot_cmd_channel_name, category=category_admin)
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


# Creates a new text channel
        delt_msg_name = "🚮-delt-msg"
        delt_msg_channel_id = read_config(config_dir,"channel", "delt_msg_channel_id", "int")
        delt_msg = discord.utils.get(guild.text_channels, id=delt_msg_channel_id)

        if delt_msg != None:
            print(f"The channel {delt_msg.name} already exists.")
        else:
            print(f"The channel {delt_msg_name} does not exist.")
            delt_msg = await guild.create_text_channel(delt_msg_name, category=category_admin)
            print(f"The channel {delt_msg.name} was created.")
            write_config(config_dir, "channel", "delt_msg_channel_id", delt_msg.id)

            was_created_list.append(delt_msg)

            embed = discord.Embed(title="🚮 delt-messages", color=0x8080ff)
            embed.set_author(name=f"@{guild.name}",icon_url=f"https://i.imgur.com/OfrhTsM.png")
            embed.set_thumbnail(url="https://i.imgur.com/6I3i9X7.png")
            embed_text = f"In the first channel, 🤖 the bot will log 📝 all deleted messages to ensure that nothing is lost.📜🔍"
            embed.add_field(name="Attention!",value=embed_text, inline=True)
            await delt_msg.send(embed=embed)


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

        @bot.event
        # this event is called when a message is sent by anyone
        async def on_message(message):
            # if the user is the client user itself, ignore the message
            await bot.process_commands(message)
            # if message.content == praefix:
            #    return

            if message.author == bot.user:
                return
            # this is the string text message of the Message
            content_m = message.content

            # this is the sender of the Message
            user = message.author
            # this is the channel of there the message is sent
            channel_m = message.channel
            channel_m_id = message.channel.id
            # this is a list of the roles from the message sender
            try:
                roles = message.author.roles
            except:
                pass
            guild = message.guild
            if message.author == bot.user:
                return

            channel_msg_block_list = []
            if channel_m_id in channel_msg_block_list:

                await message.delete()
                print(f"Message was deleted by the bot:{channel_m} {message}")

        @bot.event
        async def on_message_delete(message):

            message_author = str(message.author)
            message_content = str(message.content)
            message_channel = message.channel.name
            print("Message deleted from "+str(message_author)+" in the channel: " +
                str(message_channel)+"\n Message: "+str(message_content))

            if message.author == bot.user:
                return

            Date_Time = (time.strftime("%d_%m-%Y %H:%M"))

            embed = discord.Embed(title="Deleted message", description=(
                "am "+str(Date_Time)), color=0xff0000)
            embed.set_thumbnail(url="https://i.imgur.com/PdLm65I.png")

            embed.add_field(name=message_author,
                            value=f"channel: <#{message.channel.id}>", inline=True)
            embed.set_footer(text=message_content)
            delt_msg_channel_id = read_config(
                config_dir, "msg", "delt_msg_channel_id", "int")
            Adelt_msg_name_discord = bot.get_channel(
                delt_msg_channel_id)
            await Adelt_msg_name_discord.send(embed=embed)


bot = MyBot()
bot.run(Discord_token)