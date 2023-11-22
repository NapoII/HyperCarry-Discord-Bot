"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This cog creates automatic voice channels when the user needs them. And the user can manage them.
------------------------------------------------
"""

from discord.ext import commands, tasks
from util.__funktion__ import *
import random
import discord
from discord import app_commands
from discord import app_commands, ui


current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
config_dir = os.path.join(bot_folder, "cfg", "config.ini")
category_private_voice_id = read_config(config_dir, "category", "category_private_voice_id", "int")
json_path = os.path.join(current_dir, "channel_data.json")

help_embed = discord.Embed(title="Channel Commands",
                      description="> Show all voice channel commands\n```/vc_help```\n**Only the owner and the channel administrators have the right to execute the following commands:**\n\n> Rename the Voice Channel\n```/vc_rename {new_channel_name}```\n> Set the maximum number of users.\n```/vc_limit {new_limit}```\n> Switch the status whether the server may be deleted after leaving.\n```/vc_stay```",
                      colour=0xff8000)

help_embed.set_author(name="/vc_help")


guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1
guild = discord.Object(id=guild_id)


create_channel_id =  read_config(config_dir, "channel", "create_channel_id", "int")

if create_channel_id == None:
    create_channel_id = 1

category_private_voice_id = read_config(config_dir, "category", "category_private_voice_id", "int")
if category_private_voice_id == None:
    category_private_voice_id = 1

#channel_name_list = ["Airfield", "Bandit Camp", "Harbor", "Junkyard","Large Oil Rig","Launch Site","Lighthouse","Military Tunnels","Oil Rig","Outpost","Mining Outpost","Power Plant","Sewer Branch","Satellite Dish Array","The Dome","Train Yard","Train Tunnel Network","Water Treatment Plant"]

class channelHoper_setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir

        # Hier wird die Methode beim Start des Bots aufgerufen
        self.bot.loop.create_task(self.setup_channel_hopper())

    async def setup_channel_hopper(self):
        print ("\n --> setup_channel_hopper\n")
        await self.bot.wait_until_ready()  
        guild = self.bot.get_guild(guild_id)  

        was_created_list = []
# Creates a new category

        category_name = "--🔒🔊 - Private Voice - 🔊🔒--"
        category_private_voice_id = read_config(config_dir, "category", "category_private_voice_id", "int")
        category_private_voice = discord.utils.get(guild.categories, id=category_private_voice_id)

        if category_private_voice != None:
            print(f"The category {category_private_voice.name} already exists.")

        else:
            print(f"The category {category_name} does not yet exist and will now be created")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=True),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }
        
            category_private_voice = await guild.create_category(category_name, overwrites=overwrites)
            print(f"The category {category_name} was created.")
            category_private_voice_id = category_private_voice.id
            write_config(config_dir, "category","category_private_voice_id", category_private_voice_id)

            was_created_list.append(category_private_voice)


# Creates a new voice channel
        channel_name = "➕-create-channel-➕"
        create_channel_id = read_config(config_dir,"channel", "create_channel_id", "int")
        create_channel = discord.utils.get(guild.voice_channels, id=create_channel_id)

        if create_channel != None:
            print(f"The channel {create_channel.name} already exists.")
        else:
            print(f"The channel {channel_name} does not exist.")
            create_channel = await guild.create_voice_channel(channel_name, category=category_private_voice)
            print(f"The channel {create_channel.name} was created.")
            write_config(config_dir, "channel", "create_channel_id", create_channel.id)

            was_created_list.append(create_channel)


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
            embed = discord.Embed(title=f"The following Channel Hopper System Channels have been created:",
                                description=f"> The following channels had to be created:\n{text}\ncreated: {dc_time}",
                                colour=0xffff80)
            try:
                bot_cmd_channel_id = read_config(config_dir, "channel", "bot_cmd_channel_id", "int")
                bot_cmd_channel = guild.get_channel(bot_cmd_channel_id)
                await bot_cmd_channel.send(embed=embed)
            except:
                pass



#player_have_channel_list = []
class channelHoper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_channels = {}  # A dictionary for tracking the channels created <-- bug if restart forgott old channels
        #self.player_have_channel_list = {}
    async def create_voice_channel(self, user):
        category = discord.utils.get(user.guild.categories, id=category_private_voice_id)
        if not category:
            print(f"Category with ID {category_private_voice_id} was not found.")
            return

        guild = user.guild
        user_id = user.id
        user_name = user.name
        if is_user_in(user_id, json_path) == True:

            channel_id = get_channel_id_from(user_id, json_path)
            channel = self.bot.get_channel(channel_id)

            embed = discord.Embed(title="You already have a voice channel",
                      description=f"""> Only one voice channel per user.\n> I moved you into the channel.
                      
                      <#{channel_id}>""",
                      colour=0xff0000)

            await user.move_to(channel)
            await user.send(embed=help_embed)
            await user.send(embed=embed)

        if is_user_in(user_id, json_path) == False:
        #if user_id not in self.voice_channels.values():
            #if user.id not in self.voice_channels.values:
            # random_pic = random.choice(channel_name_list)

            new_channel = await category.create_voice_channel(f"🔊  {user_name}´s VC")
            new_channel_id = new_channel.id

            add_new_channel_data(user_name, user_id, new_channel_id, json_path)

            owner_id = find_main_key(new_channel.id, json_path)
            print(f"interaction_channel.id {new_channel.id}")
            data = read_json_file(json_path)
            limit = new_channel.user_limit
            admin_list = get_item_from_channel("admin", new_channel.id, data)
            admin_list_len = len(admin_list)
            owner = await self.bot.fetch_user(owner_id)

            
            x = -1
            admin_text = ""
            while True:
                x = x + 1
                if x == admin_list_len:
                    break
                admin = admin_list[x]
                admin_text = admin_text +f"<@{admin}> "

            stay = get_item_from_channel("stay", new_channel.id, data)
            hide = get_item_from_channel("hide", new_channel.id, data)

            embed = discord.Embed(title=f"<#{new_channel.id}>",
                                description=f"<@{owner.id}>, is the owner of this Voice Channel\nThe following User have admin rights on this channel:\n{admin_text}\n",
                                colour=0x00b0f4)

            embed.set_author(name="Channel Info")

            embed.add_field(name="Stay mode",
                            value=stay,
                            inline=True)
            embed.add_field(name="Hide mode",
                            value=hide,
                            inline=True)
            embed.add_field(name="User limit",
                            value=limit,
                            inline=True)

            embed.set_thumbnail(url="https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png")

            embed.set_footer(text="for help type /vc_help",
                 icon_url="https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png")
            channel_msg = await new_channel.send(embed=embed)

            fill_item_in_channel(new_channel.id, "channel_msg_id", channel_msg.id, json_path)

            #new_channel = await category.create_voice_channel(f"{random_pic} | {user.name}")
            await user.move_to(new_channel)
            user_img = user.display_avatar

            await new_channel.send(embed=help_embed)

            self.voice_channels[new_channel.id] = user.id



    async def delete_voice_channel(self, channel):
        if is_channel_id_in(channel.id, json_path) == True:
        # if channel.id in self.voice_channels:
            #del self.voice_channels[channel.id]
            stay_status = get_item_from_channel("stay",channel.id, json_path)
            if stay_status == False:
                delete_data_with_channel_id(channel.id, json_path)
                await channel.delete()
            if stay_status == True:
                
                admin_list = get_admin_list(channel.id, json_path)
                admin_list_len = len(admin_list)
                x = -1
                admin_text = ""
                while True:
                    x = x + 1
                    if x == admin_list_len:
                        break
                    admin = admin_list[x]
                    user = await self.bot.fetch_user(admin)
                    admin_text = admin_text + f"@{user.name} "
                embed_text = f"""The following users have the rights to do so:
                {admin_text}"""
                embed = discord.Embed(title="The channel is only deleted again when the /vc_stay command is executed", description= embed_text, color=0x00ff00)
                # Here it is assumed that 'create_channel' is the reference to the created voice channel.
                embed.set_thumbnail(url="https://i.imgur.com/to3JTGx.png")
                await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == after.channel:  # The user has not changed his language status
            return
        #create_channel_id =  read_config(config_dir, "channel", "create_channel_id", "int")
        if after.channel and after.channel.id == create_channel_id:  # The user has joined the channel being watched
            await self.create_voice_channel(member)
        #elif before.channel and before.channel.id in self.voice_channels:  # The user has left the created channel
        elif before.channel and is_channel_id_in(before.channel.id, json_path):
            channel = discord.utils.get(member.guild.voice_channels, id=before.channel.id)
            if channel and len(channel.members) == 0:
                await self.delete_voice_channel(channel)



class bot_vc_rename(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    description = "Rename the Voice Channel."

    @app_commands.command(name="vc_rename", description=description)
    @app_commands.describe(
        new_channel_name="New name for your Voice Channel.",
    )
    async def vc_rename(self , interaction: discord.Interaction, new_channel_name: str,):
        self.new_channel_name = new_channel_name

        interaction_user_id = interaction.user.id
        target_channel_id = interaction.channel.id
        if is_he_channel_admin(interaction_user_id, target_channel_id, json_path) == True:

            old_name = interaction.channel.name
            await interaction.channel.edit(name = new_channel_name)

            embed = discord.Embed(title="Channel name has been changed", description=f"""from `{old_name}` to `{new_channel_name}`.
                                    
                                <#{interaction.channel.id}>""")
            embed.set_thumbnail(url="https://i.imgur.com/bhRp1Il.png")
            msg = await interaction.response.send_message(embed=embed, ephemeral=True,)


            channel_msg_id = get_item_from_channel("channel_msg_id", target_channel_id, json_path)
            channel_msg = await interaction.channel.fetch_message(channel_msg_id)

            data = read_json_file(json_path)
            owner_id = find_main_key(interaction.channel.id, data)
            limit = interaction.channel.user_limit
            admin_list = get_item_from_channel("admin", interaction.channel.id, data)
            admin_list_len = len(admin_list)
            owner = await self.bot.fetch_user(owner_id)
        
            x = -1
            admin_text = ""
            while True:
                x = x + 1
                if x == admin_list_len:
                    break
                admin = admin_list[x]
                admin_text = admin_text +f"<@{admin}> "

            stay = get_item_from_channel("stay", interaction.channel.id, data)
            hide = get_item_from_channel("hide", interaction.channel.id, data)


            embed = discord.Embed(title=f"<#{interaction.channel.id}>",
                                description=f"<@{owner.id}>, is the owner of this Voice Channel\nThe following User have admin rights on this channel:\n{admin_text}\n",
                                colour=0x00b0f4)

            embed.set_author(name="Channel Info")

            embed.add_field(name="Stay mode",
                            value=stay,
                            inline=True)
            embed.add_field(name="Hide mode",
                            value=hide,
                            inline=True)
            embed.add_field(name="User limit",
                            value=limit,
                            inline=True)

            embed.set_thumbnail(url="https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png")

            embed.set_footer(text="for help type /vc_help",
                 icon_url="https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png")
            await channel_msg.edit(embed=embed)

        else:
            if len(get_list_for_all_admin_server_from_user(interaction_user_id, json_path)) <= 0:
                embed=discord.Embed(title="You do not have a channel with admin rights", description=f"""You can create a channel by jumping into the create channel:      
                                        <#{create_channel_id}>""", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/LFG51bE.png")
                msg = await interaction.response.send_message(embed=embed, ephemeral=True,)


            else:
                channel_id_list = get_list_for_all_admin_server_from_user(interaction_user_id,json_path)
                channel_id_list_len = len(channel_id_list)
                x = -1
                channel_id_ist_in_str = ""
                while True:
                    x = x + 1
                    if x == channel_id_list_len:
                        break
                    channel_id_ist_in_str = channel_id_ist_in_str + f"<#{channel_id_list[x]}>\n"
                
                embed=discord.Embed(title="You write the commands in the wrong channel", description=f"""These are all channels in which you have admin rights:      
                                        {channel_id_ist_in_str}
write the command in the desired channel.""", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/LFG51bE.png")
                msg = await interaction.response.send_message(embed=embed, ephemeral=True,)



class bot_vc_limit(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    description = "Set the maximum number of users."

    @app_commands.command(name="vc_limit", description=description)
    @app_commands.describe(
        new_limit="Set the limit of users in a channel.",
    )
    async def vc_limit(self, interaction: discord.Interaction, new_limit: int,):
        self.new_limit = new_limit
        interaction_user_id = interaction.user.id
        interaction_channel = interaction.channel

        if is_he_channel_admin(interaction_user_id, interaction_channel.id, json_path) == True:
            channel_id = get_channel_id_from(interaction_user_id, json_path)
            channel = self.bot.get_channel(channel_id)

            old_limit = channel.user_limit 
            await channel.edit(user_limit=new_limit)

            embed=discord.Embed(title="Channel limit has been changed", description=f"""from `{old_limit}` to `{new_limit}`.
                                    
                                <#{channel_id}>""", color=0xfffff)
            embed.set_thumbnail(url="https://i.imgur.com/bhRp1Il.png")
            msg = await interaction.response.send_message(embed=embed, ephemeral=True)

            target_channel_id = interaction.channel.id
            channel_msg_id = get_item_from_channel("channel_msg_id", target_channel_id, json_path)
            channel_msg = await interaction.channel.fetch_message(channel_msg_id)

            data = read_json_file(json_path)
            owner_id = find_main_key(interaction.channel.id, data)
            limit = interaction.channel.user_limit
            admin_list = get_item_from_channel("admin", interaction.channel.id, data)
            admin_list_len = len(admin_list)
            owner = await self.bot.fetch_user(owner_id)
        
            x = -1
            admin_text = ""
            while True:
                x = x + 1
                if x == admin_list_len:
                    break
                admin = admin_list[x]
                admin_text = admin_text +f"<@{admin}> "

            stay = get_item_from_channel("stay", interaction.channel.id, data)
            hide = get_item_from_channel("hide", interaction.channel.id, data)


            embed = discord.Embed(title=f"<#{interaction.channel.id}>",
                                description=f"<@{owner.id}>, is the owner of this Voice Channel\nThe following User have admin rights on this channel:\n{admin_text}\n",
                                colour=0x00b0f4)

            embed.set_author(name="Channel Info")

            embed.add_field(name="Stay mode",
                            value=stay,
                            inline=True)
            embed.add_field(name="Hide mode",
                            value=hide,
                            inline=True)
            embed.add_field(name="User limit",
                            value=limit,
                            inline=True)

            embed.set_thumbnail(url="https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png")

            embed.set_footer(text="for help type /vc_help",
                 icon_url="https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png")
            await channel_msg.edit(embed=embed)

        else:
            if len(get_list_for_all_admin_server_from_user(interaction_user_id, json_path)) <= 0:
                embed=discord.Embed(title="You do not have a channel with admin rights", description=f"""You can create a channel by jumping into the create channel:      
                                        <#{create_channel_id}>""", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/LFG51bE.png")
                msg = await interaction.response.send_message(embed=embed, ephemeral=True,)


            else:
                channel_id_list = get_list_for_all_admin_server_from_user(interaction_user_id,json_path)
                channel_id_list_len = len(channel_id_list)
                x = -1
                channel_id_ist_in_str = ""
                while True:
                    x = x + 1
                    if x == channel_id_list_len:
                        break
                    channel_id_ist_in_str = channel_id_ist_in_str + f"<#{channel_id_list[x]}>\n"
                
                embed=discord.Embed(title="You write the commands in the wrong channel", description=f"""These are all channels in which you have admin rights:      
                                        {channel_id_ist_in_str}
write the command in the desired channel.""", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/LFG51bE.png")
                msg = await interaction.response.send_message(embed=embed, ephemeral=True,)


class bot_vc_stay(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    description = "Switch the status whether the server may be deleted after leaving"

    @app_commands.command(name="vc_stay", description=description)

    async def vc_stay(self, interaction: discord.Interaction):
        interaction_user_id = interaction.user.id
        interaction_channel = interaction.channel

        if is_he_channel_admin(interaction_user_id, interaction_channel.id, json_path) == True:
            channel_id = get_channel_id_from(interaction_user_id, json_path)
            channel = self.bot.get_channel(channel_id)


            new_stay_status = switch_stay_status(channel_id, json_path)
            if new_stay_status == True:
                text = "The channel is now not deleted when empty."
            else:
                text = "The channel is now deleted again when it is empty"

            embed=discord.Embed(title="Stay status was changed..", description=f"""{text}
                                    
                                <#{channel_id}>""", color=0xfffff)
            embed.set_thumbnail(url="https://i.imgur.com/bhRp1Il.png")
            msg = await interaction.response.send_message(embed=embed, ephemeral=True)

            target_channel_id = interaction.channel.id
            channel_msg_id = get_item_from_channel("channel_msg_id", target_channel_id, json_path)
            channel_msg = await interaction.channel.fetch_message(channel_msg_id)

            data = read_json_file(json_path)
            owner_id = find_main_key(interaction.channel.id, data)
            limit = interaction.channel.user_limit
            admin_list = get_item_from_channel("admin", interaction.channel.id, data)
            admin_list_len = len(admin_list)
            owner = await self.bot.fetch_user(owner_id)
        
            x = -1
            admin_text = ""
            while True:
                x = x + 1
                if x == admin_list_len:
                    break
                admin = admin_list[x]
                admin_text = admin_text +f"<@{admin}> "

            stay = get_item_from_channel("stay", interaction.channel.id, data)
            hide = get_item_from_channel("hide", interaction.channel.id, data)


            embed = discord.Embed(title=f"<#{interaction.channel.id}>",
                                description=f"<@{owner.id}>, is the owner of this Voice Channel\nThe following User have admin rights on this channel:\n{admin_text}\n",
                                colour=0x00b0f4)

            embed.set_author(name="Channel Info")

            embed.add_field(name="Stay mode",
                            value=stay,
                            inline=True)
            embed.add_field(name="Hide mode",
                            value=hide,
                            inline=True)
            embed.add_field(name="User limit",
                            value=limit,
                            inline=True)

            embed.set_thumbnail(url="https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png")

            embed.set_footer(text="for help type /vc_help",
                 icon_url="https://raw.githubusercontent.com/NapoII/HyperCarry-Discord-Bot/main/HyperCarry-Discord-Bot/img/iCarry_Avatar.png")
            await channel_msg.edit(embed=embed)

            
        else:
            if len(get_list_for_all_admin_server_from_user(interaction_user_id, json_path)) <= 0:
                embed=discord.Embed(title="You do not have a channel with admin rights", description=f"""You can create a channel by jumping into the create channel:      
                                        <#{create_channel_id}>""", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/LFG51bE.png")
                msg = await interaction.response.send_message(embed=embed, ephemeral=True,)


            else:
                channel_id_list = get_list_for_all_admin_server_from_user(interaction_user_id,json_path)
                channel_id_list_len = len(channel_id_list)
                x = -1
                channel_id_ist_in_str = ""
                while True:
                    x = x + 1
                    if x == channel_id_list_len:
                        break
                    channel_id_ist_in_str = channel_id_ist_in_str + f"<#{channel_id_list[x]}>\n"
                
                embed=discord.Embed(title="You write the commands in the wrong channel", description=f"""These are all channels in which you have admin rights:      
                                        {channel_id_ist_in_str}
write the command in the desired channel.""", color=0xff0000)
                embed.set_thumbnail(url="https://i.imgur.com/LFG51bE.png")
                msg = await interaction.response.send_message(embed=embed, ephemeral=True,)


class bot_vc_kick(commands.Cog):
    def __init__(self, bot: commands.Bot, interaction: discord.Interaction) -> None:
        self.bot = bot

    members = discord.VoiceChannel.members

    description = "Kick a user from your Channel"
    
    @app_commands.command(name="vc_kick", description=description)
    @app_commands.describe(player_to_kick='Player choose')
    @app_commands.choices(player_to_kick=[
        discord.app_commands.Choice(name='Blue', value=1),
        discord.app_commands.Choice(name='Green', value=3)])
    
    async def choisecolor(self, interaction: discord.Interaction, player_to_kick: discord.app_commands.Choice[int]):
        # code for kick the user.id ....
        await interaction.response.send_message(f"test {player_to_kick.name}")                                                                                                                                                  


class bot_vc_help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    description = "Shows you a list of all commands and your channels on which you are an administrator"

    @app_commands.command(name="vc_help", description=description)

    async def vc_help(self, interaction: discord.Interaction):

        interaction_user_id = interaction.user.id
        interaction_channel = interaction.channel

        msg = await interaction.channel.send(embed=help_embed)

        list_of_admin_channel_from_user = get_list_for_all_admin_server_from_user(interaction_user_id, json_path)
        list_of_admin_channel_from_user_len = len(list_of_admin_channel_from_user)
        try:
            if list_of_admin_channel_from_user_len != 0:
                x = -1
                list_text = ""
                while True:
                    x = x + 1
                    if x == list_of_admin_channel_from_user_len:
                        break
                    list_text = list_text +f"<#{list_of_admin_channel_from_user[x]}>\n"


                embed = discord.Embed(title="List of all your channels with administrator rights",
                        description=f"{list_text}")
                msg = await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="You don't have a voice channel or right for one at the moment", description=f"But you can create one under <#{create_channel_id}>")
            
            msg = await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
            pass


async def setup(bot: commands.Bot):
    await bot.add_cog(channelHoper_setup(bot), guild=discord.Object(guild_id))
    await bot.add_cog(channelHoper(bot), guild=discord.Object(guild_id))
    await bot.add_cog(bot_vc_rename(bot), guild=discord.Object(guild_id))
    await bot.add_cog(bot_vc_limit(bot), guild=discord.Object(guild_id))
    await bot.add_cog(bot_vc_stay(bot), guild=discord.Object(guild_id))
    await bot.add_cog(bot_vc_help(bot), guild=discord.Object(guild_id))
    # await bot.add_cog(bot_vc_kick(bot), guild=discord.Object(guild_id))


