import discord
from discord.ext import commands
import pyautogui
token = "MTE3MjAxNzY1MjY1MTI2NjE0MA.G-ttYq.FjEurwUxl-hcSN0ZanCepDh9MhKkh8vczmVPnw"
SERVER_ID = '1103399447100133386'

1173923194235785286
intents = discord.Intents.default()
intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user.name} ({bot.user.id})')

    # Den Server mit der angegebenen ID abrufen
    server = bot.get_guild(int(SERVER_ID))
    print("\n")
    print(f'Erfolgreich zum Server {server.name} verbunden')
    print(f"Server : {server.name}\n")
    print("\n")
    do_it = pyautogui.confirm(text=f'Server : {server.name}', title='Correct server?', buttons=['OK', 'Cancel'])

    if do_it == 'OK':

        if server:
            
            channel_list = [channel.id for channel in server.channels]
            print('channel-IDs:', channel_list)
            print("\n")
            channel_list_len = len(channel_list)
            x = -1
            while True:
                x = x + 1
                if x == channel_list_len:
                    break
                channel = bot.get_channel(channel_list[x])
                await bot.get_channel(channel_list[x]).delete()

                print(f"-->> delt: {channel.name} - #{channel_list[x]}")
        
            
        else:
            print(f'Server mit ID {SERVER_ID} nicht gefunden')
    else:
        pass
    print("\n")
    print("Done !")
    print("\n")
# Füge deinen Token hier ein
bot.run(token)
