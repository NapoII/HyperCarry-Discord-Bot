import discord
from discord.ext import commands
guild_id = 1103399447100133386
toekn = "MTE3MjAxNzY1MjY1MTI2NjE0MA.GdOdl5._XdcF4KFyWcVS8Nh4z5W85cNwwEHQTkrklcTKU"
intents = discord.Intents.default()
intents.all()

bot = commands.Bot(command_prefix="your_prefix", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await remove_existing_commands(bot, guild_id=guild_id)

async def remove_existing_commands(bot, guild_id):
    commands = await bot.http.get_guild_commands(bot.user.id, guild_id)

    for command in commands:
        await bot.http.delete_guild_command(bot.user.id, guild_id, command['id'])
        print(f"Command {command['name']} removed.")

# Starte den Bot

    

# Starte den Bot
bot.run(toekn)


