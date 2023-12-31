"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This COG is for embed a help information for Rust.
exampel : cctv codes
------------------------------------------------
"""

from discord.ext import commands, tasks
from util.__funktion__ import *
import discord
from discord import app_commands
from discord import app_commands, ui
from discord.ext import commands
from discord.ui import Select, View

# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")

json_path_ticket = os.path.join(current_dir, "ticket_data.json")
json_path_support = os.path.join(current_dir, "support_team_data.json")


guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1


class Send_embed_Modal(discord.ui.Modal, title='Send Embed'):
    print(f"/send_embed  --> send Modal")
    Title = None
    Image_URL = None
    Thumbnail_URL = None
    description = ""
    hex_COLUR = None
    
    channel_taregt_id = discord.ui.TextInput(label='Channel ID', required=True, style=discord.TextStyle.short)
    Title = discord.ui.TextInput(label='Title', required=False)
    #Thumbnail_URL = discord.ui.TextInput(label='Thumbnail URL', style=discord.TextStyle.short, required=False)
    Image_URL = discord.ui.TextInput(label='Image URL', style=discord.TextStyle.short, required=False)
    description = discord.ui.TextInput(label='Description', style=discord.TextStyle.paragraph, required=False, default="", placeholder="Write the content of the embed.")
    hex_COLUR = discord.ui.TextInput( label='HEX COLOUR', default="80ffff", style=discord.TextStyle.short, required=False)
    
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Submission entered.", ephemeral=True)

    async def on_submit(self, interaction: discord.Interaction):


        channel_taregt_id = self.channel_taregt_id.value
        Title = self.Title.value
        Image_URL = self.Image_URL.value
        description = self.description.value
        hex_COLUR = self.hex_COLUR.value

        print(f"""/send_embed  --> embed Setting:
              Title = {Title}
              channel_taregt_id = {channel_taregt_id}
              Image_URL = {Image_URL}
              description = {description}
              hex_COLUR = {hex_COLUR}""")
        
        embed = discord.Embed(title=f"{Title}",
                      description=f"{description}",
                      colour=int(hex_COLUR,16))
        
        if Image_URL != None:
            embed.set_image(url=f"{Image_URL}")

        view = Confirm_say()
        test_embed_msg = await interaction.response.send_message(embed=embed, view=view)


        await view.wait()
        if view.value is None:
            self.confirm_Button = False
            print(f'Timed out... self.confirm_Button = {self.confirm_Button}')

        elif view.value:
            self.confirm_Button = True
            
            try:
                target = discord.utils.get(interaction.guild.text_channels, id=int(channel_taregt_id))
                await target.send(embed=embed)
                await interaction.channel.last_message.edit(content=f"**Embed was sent to <#{target.id}>**", view=None)
            except:
                embed = discord.Embed(description=f"**The Channel with the ID does not exist: <#{channel_taregt_id}>**",
                                    colour=0xf40006)
                await interaction.channel.last_message.edit(embed=embed, view=None)

           
        else:
            self.confirm_Button = False
            print(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
            # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text




class say_bot_send(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    description = "Send an embed to a text channel"
    @app_commands.command(name="send_embed", description=description, )

    async def send_embed_bot(self, interaction: discord.Interaction):

        print(f"/send_embed  --> user: {interaction.user.name}")
        await interaction.response.send_modal(Send_embed_Modal())




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
    await bot.add_cog(say_bot_send(bot), guild=discord.Object(guild_id))