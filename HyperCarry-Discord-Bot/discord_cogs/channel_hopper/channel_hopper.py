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

# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")
category_private_voice_id = int(read_config(config_dir, "channel", "category_private_voice_id"))
json_path = os.path.join(current_dir, "channel_data.json")

vc_user_command_list = f"""
- The owner can rename the channel with
`/vc name`
- The owner can limit the channel with
`/vc limit x` (0 = infinite, X = number up to 99)
- The owner can hide the channel from everyone with
`/vc hide` or show it with `/vc unhide`
- The owner can mute, kick and ban other members in the channel with
`/vc kick name`, `/vc ban name`"""


guild_id = read_config(config_dir, "client", "guild_id")
if guild_id == None:
    guild_id = 1
guild_id = int(guild_id)
guild = discord.Object(id=guild_id)


create_channel_id =  read_config(config_dir, "channel", "create_channel_id")

if create_channel_id == None:
    create_channel_id = 1
create_channel_id = int(create_channel_id)

category_private_voice_id = read_config(config_dir, "channel", "category_private_voice_id")
if category_private_voice_id == None:
    category_private_voice_id = 1
category_private_voice_id = int(category_private_voice_id)

#channel_name_list = ["Airfield", "Bandit Camp", "Harbor", "Junkyard","Large Oil Rig","Launch Site","Lighthouse","Military Tunnels","Oil Rig","Outpost","Mining Outpost","Power Plant","Sewer Branch","Satellite Dish Array","The Dome","Train Yard","Train Tunnel Network","Water Treatment Plant"]

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
            await user.move_to(channel)
            embed=discord.Embed(title="Only one voice channel per user allowed", description=f"""You already have a voice channel. 
                                <#{channel_id}>
                                I switched you to the channel.
                                you can edit your channel with:
                                {vc_user_command_list}""", color=0xff0000)
            embed.set_thumbnail(url="https://i.imgur.com/LFG51bE.png")
            await user.send(embed=embed)

        if is_user_in(user_id, json_path) == False:
        #if user_id not in self.voice_channels.values():
            #if user.id not in self.voice_channels.values:
            # random_pic = random.choice(channel_name_list)

            new_channel = await category.create_voice_channel(f"🔊  {user_name}´s VC")

            new_channel_id = new_channel.id



            add_new_channel_data(user_name, user_id, new_channel_id, json_path)

            #new_channel = await category.create_voice_channel(f"{random_pic} | {user.name}")
            await user.move_to(new_channel)
            user_img = user.display_avatar
            embed_text = f"""- `{user_name}` is the channel owner from
            <#{new_channel.id}>.

He can edit the channel with the following commands:
{vc_user_command_list}"""
            embed = discord.Embed(title="Commands to edit the channel:", description= embed_text, color=0x00ff00)

            # Here it is assumed that 'create_channel' is the reference to the created voice channel.
            embed.set_thumbnail(url=user_img)
            await new_channel.send(embed=embed)
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

    description = "Rename your voice channel."

    @app_commands.command(name="vc_rename", description=description)
    @app_commands.describe(
        new_channel_name="New name for your Voice Channel.",
    )
    async def vc_rename(self, interaction: discord.Interaction, new_channel_name: str,):
        self.new_channel_name = new_channel_name

        interaction_user_id = interaction.user.id
        target_channel_id = interaction.channel.id
        if is_he_channel_admin(interaction_user_id, target_channel_id, json_path) == True:

            old_name = interaction.channel.name
            await interaction.channel.edit(name= new_channel_name)

            embed=discord.Embed(title="Channel name has been changed", description=f"""from `{old_name}` to `{new_channel_name}`.
                                    
                                <#{interaction.channel.id}>
                                    
                                    you can edit your channel with:
                                    {vc_user_command_list}""", color=0xfffff)
            embed.set_thumbnail(url="https://i.imgur.com/bhRp1Il.png")
            msg = await interaction.response.send_message(embed=embed, ephemeral=True,)
        
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
                                    
                                <#{channel_id}>
                                    
                                    you can edit your channel with:
                                    {vc_user_command_list}""", color=0xfffff)
            embed.set_thumbnail(url="https://i.imgur.com/bhRp1Il.png")
            msg = await interaction.response.send_message(embed=embed, ephemeral=True, )
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
                                    
                                <#{channel_id}>
                                    
                                    you can edit your channel with:
                                    {vc_user_command_list}""", color=0xfffff)
            embed.set_thumbnail(url="https://i.imgur.com/bhRp1Il.png")
            msg = await interaction.response.send_message(embed=embed, ephemeral=True, )
            
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


class bot_vc_status(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    description = "Displays the status of the voice channel"

    @app_commands.command(name="vc_status", description=description)

    async def vc_stay(self, interaction: discord.Interaction):
        interaction_user_id = interaction.user.id
        interaction_channel = interaction.channel

        owner_id = find_main_key(json_path, interaction_channel.id)
        print(f"interaction_channel.id {interaction_channel.id}")
        data = read_json_file(json_path)
        channel_name = interaction_channel.name
        admin_list = get_item_from_channel("admin", interaction_channel.id, data)
        admin_list_len = len(admin_list)
        x = -1
        admin_text = ""
        while True:
            x = x + 1
            if x == admin_list_len:
                break
            admin = admin_list[x]
            admin_text = admin_text +f"@{admin} "

        stay = get_item_from_channel("stay", interaction_channel.id, data)
        hide = get_item_from_channel("hide", interaction_channel.id, data)



        embed = discord.Embed(title="Voice Channel Status",
                    colour=0x00b0f4)

        embed.set_author(name=interaction.user.name,
                        icon_url=interaction.user.display_avatar)

        embed.add_field(name="Channel Name:",
                        value=channel_name,
                        inline=False)
        embed.add_field(name="Admin rights",
                        value=admin_text,
                        inline=False)
        embed.add_field(name="Stay status",
                        value=stay,
                        inline=True)
        embed.add_field(name="Hide statsus",
                        value=hide,
                        inline=True)
        msg = await interaction.response.send_message(embed=embed, ephemeral=True)


        embed = discord.Embed(title="This is not a private voice channel",
                            description=f"You are not in a private Voice channel and can therefore not display a status, go to the <#{category_private_voice_id}> area for this.")

        embed.set_thumbnail(url="https://i.imgur.com/LFG51bE.png")
        msg = await interaction.response.send_message(embed=embed, ephemeral=True)
    




async def setup(bot: commands.Bot):
    await bot.add_cog(channelHoper(bot), guild=discord.Object(guild_id))
    await bot.add_cog(bot_vc_rename(bot), guild=discord.Object(guild_id))
    await bot.add_cog(bot_vc_limit(bot), guild=discord.Object(guild_id))
    await bot.add_cog(bot_vc_stay(bot), guild=discord.Object(guild_id))
    #await bot.add_cog(bot_vc_status(bot), guild=discord.Object(guild_id))


