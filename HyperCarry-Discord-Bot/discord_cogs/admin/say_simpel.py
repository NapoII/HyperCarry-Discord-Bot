import discord

# Deine Discord-Bot-Token hier einfügen
TOKEN = "MTE3MjAxNzY1MjY1MTI2NjE0MA.GBv9XO.euJBoXegu5t3j7T9dG_L29wHyGj7K26CYrL5Nw"

# Deine vorgegebene Channel-ID hier einfügen
CHANNEL_ID = 695743343841247252

website_url = "discord.gg/gGjW9AY"

# Initialisierung des Discord-Clients
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Eingeloggt als {client.user.name}')
    channel = client.get_channel(CHANNEL_ID)

    # Erstelle ein Embed
    embed = discord.Embed(
        title='Hello HyperCarry Player',
        description="""🎉Hello <@&1102063023516033114> Gamers! 🎮

🚨 Exciting news!🚨

Our server will now automatically and instantly reboot in case of a crash.

🔄 No more worries about downtime! 🔄

Have Fun!
Your HyperCarry Team <3


""",
        color=discord.Color.blue()  # Farbe des Embeds
    )

    # Set the image URL in the embed
    image_url = "https://i.imgur.com/n7YoHaF.png"
    embed.set_image(url=image_url)

    # Add a field with a link
    website_url = "https://napoii.github.io/Rust-Collection/"
    embed.add_field(name="HyperCarry Community #1 GunGame [GG]",
                    value=f"```steam://connect/213.239.210.121:27020```")
    embed.add_field(name="HyperCarry Community #2 GunGame [GG]",
                    value=f"```steam://connect/213.239.210.121:27030```")
    content = "  <@&1102063023516033114>"
    await channel.send(content = content, embed=embed)

client.run(TOKEN)
