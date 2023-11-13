class bot_vc_kick(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    description = "Kick a user from your Channel"
    
    @app_commands.command(name="vc_kick", description=description)
    @app_commands.describe(colors='Colors to choose from')
    @app_commands.choices(colors=[
        discord.app_commands.Choice(name='Blue', value=2),
        discord.app_commands.Choice(name='Green', value=3)])
    
    async def choisecolor(self, interaction: discord.Interaction, colors: discord.app_commands.Choice[int]):
        await interaction.response.send_message(f"farbe {colors.name}")                                                                                  
