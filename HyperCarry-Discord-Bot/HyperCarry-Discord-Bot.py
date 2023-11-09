"""Full Doku on: https://github.com/NapoII/HyperCarry-Disocrd-Bot"
-----------------------------------------------
!!! ADD MUST HAVE INFO !!
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
        guild_id = int(read_config(config_dir, "client", "guild_id"))
        guild = discord.Object(id=guild_id)
        praefix = read_config(config_dir, "client", "praefix")
        activity_text = (read_config(config_dir, "client", "activity"))
        activity = Discord_Activity(activity_text)
        break
    except:
        print(f"Fill in the empty fields in both config files! \n token_config -> [{token_config_dir}]\nconfig_dir -> [{config_dir}]")

# Channel
admin_channel_id = int(read_config(config_dir, "channel", "admin_channel_id"))
delt_messages_channel_id = int(read_config(config_dir, "channel", "delt_messages_channel_id"))



################################################################################################################################

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=praefix,
            intents=discord.Intents.all(),
            application_id=Application_ID,
            activity=activity)

        # "Work_Folder.Rust.test",
        #"discord_cogs.Rust.player_watch",
        self.initial_extensions = [
            
        ]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild=discord.Object(guild_id))

    async def on_ready(self):
        print("Discord Bot prints in | wait_until_ready")
        await self.wait_until_ready()
        print(f'printged in as {self.user} (ID: {self.user.id})')

        for guild in bot.guilds:



            # Searches all existing categories on the server for the category with the name "Rust".
            category_name = "--------💻 - Admin - 💻--------"
            category_admin = discord.utils.get(guild.categories, name=category_name)

            if category_admin is not None:

                print(f"The category {category_admin.name} already exists.")

            else: 
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=True),  # Everyone can view the category
                    guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
                }

                print(f"The category {category_name} does not yet exist and will now be created")
                # Creates a new category
                category_admin = await guild.create_category(category_name, overwrites=overwrites)
                print(f"The category {category_name} was created.")
                category_admin_name = category_admin.name
                category_admin_id = category_admin.id
                write_config(config_dir, "channel","category_admin_id", category_admin_id)

                icarry_cmd = await guild.create_text_channel("💻-icarry-cmd ", category=category_admin)
                print(f"The channel {icarry_cmd.name} was created.")

                icarry_cmd_id_name = icarry_cmd.name
                icarry_cmd_id = icarry_cmd.id
                write_config(config_dir, "Channel","icarry_cmd_id", icarry_cmd_id)
                #write_config(config_dir, "Channel", "icarry_cmd_id_name", icarry_cmd_id_name)

                embed = discord.Embed(title="Attention!", color=0x8080ff)
                embed.set_author(name=f"@{guild.name}",
                                icon_url=f"https://i.imgur.com/OfrhTsM.png")
                embed.set_thumbnail(url="https://i.imgur.com/s5ZWwpZ.png")
                embed_text = f"🔒 Please make sure to adjust the role settings for <#{category_admin_id}> to restrict channel visibility to authorized users, instead of allowing it to be visible to everyone. 🔓"
                embed.add_field(name="Attention!",value=embed_text, inline=True)
                await icarry_cmd.send(embed=embed)

                delt_messages = await guild.create_text_channel("🚮 delt-messages", category=category_admin)
                print(f"The channel {delt_messages.name} was created.")
                delt_messages_channel_id = delt_messages.id
                delt_messages_name = delt_messages.name
                write_config(config_dir, "Channel","delt_messages_channel_id", delt_messages_channel_id)
                #write_config(config_dir, "Channel", "delt_messages_channel_name", delt_messages_name)
                print(f"The channel {delt_messages_name} was created.")

                embed = discord.Embed(title="🚮 delt-messages", color=0x8080ff)
                embed.set_author(name=f"@{guild.name}",icon_url=f"https://i.imgur.com/OfrhTsM.png")
                embed.set_thumbnail(url="https://i.imgur.com/6I3i9X7.png")
                embed_text = f"In the first channel, 🤖 the bot will log 📝 all deleted messages to ensure that nothing is lost.📜🔍"
                embed.add_field(name="Attention!",value=embed_text, inline=True)
                await delt_messages.send(embed=embed)


                embed = discord.Embed(
                    title="🍾Nice, the bot has created the required channels for the HyperCarry-DC🍾", color=0xff8080)
                embed.add_field(name="💻Restart the Bot Now💻",
                                value="So that the bot can run his routine", inline=True)
                await icarry_cmd.send(embed=embed)



        text = f"\n\nThe Bot: [ {self.user} | ID:{self.user.id} ] is connected to [{guild.name}] id: [{guild.id}]\nActivity_text:[{activity_text}]\n\n📶 Bot is Online and Rdy to Run... 📶 \n"

        admin_channel_id = int(read_config(config_dir, "channel", "admin_channel_id"))
        channel = self.get_channel(admin_channel_id)
        print(str(text))

        embed = discord.Embed(title=py_name, color=0xff80ff)
        embed.set_author(name="created by Napo_II",
                         url="https://github.com/NapoII/HyperCarry-Disocrd-Bot")
        embed.set_thumbnail(url="https://i.imgur.com/hcVwvZF.png")
        embed.add_field(name="Version", value=v, inline=True)
        embed.add_field(
            name="python", value=f"{python_version()}", inline=True)
        embed.add_field(name="github", value="https://github.com/NapoII/HyperCarry-Discord-Bot", inline=False)
        await channel.send(embed=embed)

        embed = discord.Embed(
            title="📶 Bot is Online and Rdy to Run... 📶", color=0xff8080)
        embed.add_field(name="client.name", value=self.user.name, inline=True)
        embed.add_field(name="guild.name", value=guild.name, inline=True)
        embed.add_field(name="guild.id", value=str(guild.id), inline=True)
        await channel.send(embed=embed)

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

            print(str(user) + ": (#" + str(channel_m)+") say: " + content_m)
            rust_info_channel_id = int(read_config(
                config_dir, "Channel", "rust_info_channel_id"))
            player_observation_channel_id = int(read_config(
                config_dir, "Channel", "player_observation_channel_id"))
            print(
                f"channel_m_id= {channel_m_id} == icarry_cmd_id_name= {rust_info_channel_id}")
            if channel_m_id == rust_info_channel_id or channel_m_id == player_observation_channel_id:

                await message.delete()
                print(f"Message was deleted by the bot:{channel_m} {message}")

        @bot.event
        async def on_message_delete(message):

            message_author = str(message.author)
            message_channel = "#" + str(message.channel)
            message_content = str(message.content)

            print("Message deleted from "+str(message_author)+" in the channel: " +
                str(message_channel)+"\n Message: "+str(message_content))

            if message.author == bot.user:
                return

            Date_Time = (time.strftime("%d_%m-%Y %H:%M"))

            embed = discord.Embed(title="Deleted message", description=(
                "am "+str(Date_Time)), color=0xff0000)
            embed.set_thumbnail(url="https://i.imgur.com/PdLm65I.png")

            embed.add_field(name=message_author,
                            value="Channel: "+message_channel, inline=True)
            embed.set_footer(text=message_content)
            delt_messages_channel_id = int(read_config(
                config_dir, "Channel", "delt_messages_channel_id"))
            Adelt_messages_name_discord = bot.get_channel(
                delt_messages_channel_id)
            await Adelt_messages_name_discord.send(embed=embed)


bot = MyBot()
bot.run(Discord_token)