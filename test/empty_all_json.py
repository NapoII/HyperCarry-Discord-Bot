import json
import os

def overwrite_json(file_path):
    data = {}
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def main():
    # List of JSON file paths
    json_files = [r'E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\ticket_system\support_team_data.json',
                  r'E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\game_server\server_channel_data.json',
                  r'E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\ticket_system\support_team_data.json',
                  r'E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\game_server\server_channel_data.json'
                  ]

    for file_path in json_files:
        if os.path.exists(file_path):
            overwrite_json(file_path)
            print("\n")
            print(f'Content of {file_path} has been overwritten')
        else:
            print("\n")
            print(f'The file {file_path} does not exist.')

if __name__ == "__main__":
    main()