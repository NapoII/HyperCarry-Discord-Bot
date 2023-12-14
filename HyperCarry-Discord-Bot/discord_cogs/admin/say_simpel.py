import discord


"""

https://embed.dan.onl/


"""


# Deine Discord-Bot-Token hier einfügen
token = "MTEwMzQwNzU1MDkxOTA4NjE1MQ.G2cEZ7.c7nhZNq6lBi_x9zLcH4tAvcsOXc079xY01ui7I"

# rust # token = "MTEwMzQwNzU1MDkxOTA4NjE1MQ.G2cEZ7.c7nhZNq6lBi_x9zLcH4tAvcsOXc079xY01ui7I"

# Deine vorgegebene Channel-ID hier einfügen
CHANNEL_ID = 1152263133109424159

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


    embed = discord.Embed(title="SoundBoard",
                        description="🔊 Attention Discord Adventurers!\n\n🎉 Exciting news! Our server just became a hub of multimedia delight with the arrival of Rust Soundboard and Stickers, courtesy of @Rust Team! 🤩🎮\n\n🔗 Unleash chaos and camaraderie:\n\n    🚀 Trigger your mates in-game with iconic Rust sounds\n    🎭 Spice up conversations with hilarious stickers\n    🎁 Experience laughter, surprises, and epic moments together",
                        colour=0xffffff)

    embed.set_image(url="https://i.imgur.com/MAbb5Ca.png")
    await channel.send(embed=embed)














client.run(token)
