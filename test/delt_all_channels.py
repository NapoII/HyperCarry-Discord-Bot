import discord
from discord.ext import commands
import pyautogui
token = "MTE4MDI1NzUwODQ2NDU0NTk0NA.GT1Pem.fzK4-5L-vrWN-CQf1Q8_c7iXfigIb1dLlaBa9s"
application_id = 1180257508464545944
SERVER_ID = "1179423438700564480"

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
    print(f'Successfully connected to server {server.name}')
    print(f"Server : {server.name}\n")
    print("\n")
    do_it = pyautogui.confirm(text=f'Server : {server.name}', title='Correct server?', buttons=['OK', 'Cancel'])

    if do_it == 'OK':

        if server:
            
            channel_list = [channel.id for channel in server.channels]
            channel_list_len = len(channel_list)
            x = -1
            while True:
                x = x + 1
                if x == channel_list_len:
                    break
                channel = bot.get_channel(channel_list[x])
                await bot.get_channel(channel_list[x]).delete(reason = "for test restart")

                print(f"-->> delt: {channel.name} - #{channel_list[x]}")

            
            roles_list = server.roles
            roles_list_len = len(roles_list)
            for role in roles_list:
                try:
                    await role.delete()
                    print(f"-->> deleted: {role.name} - #{role.id}")
                except Exception as e:
                    print(f"Failed to delete role {role.name}: {e}")
                    
        else:
            print(f'Server with ID {SERVER_ID} not found')
    else:
        pass
    
    print(f"""Done!\nNum of delt channels: {channel_list_len}\nNum of delt Rols: {roles_list_len}""")

bot.run(token)
