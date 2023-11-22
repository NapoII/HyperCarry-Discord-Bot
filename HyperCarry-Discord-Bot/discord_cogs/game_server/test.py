import requests

def get_server_list(api_key, filter_param):
    #url = "https://api.steampowered.com/IGameServersService/GetAccountPublicInfo/v1/"
    url = "https://api.steampowered.com/IGameServersService/GetServerList/v1/"
    params = {
        'key': api_key,
        'filter': f"addr\\{filter_param}"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


api_key = "6F7E8FB39DEB8BC9D3945C867D379020"
filter_param = "213.239.210.121:27020"

server_list = get_server_list(api_key, filter_param)

# print(server_list["response"]["servers"][0]["addr"])


import json



def add_server_data(json_path, server_address, channel_id):
    # Read the existing JSON data
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Find the highest existing key
    max_key = max(map(int, data.keys())) if data else 0

    # Create a new key (one higher than the highest existing key)
    new_key = str(max_key + 1)

    # Add the new entry
    data[new_key] = {
        "server_address": server_address,
        "channel_id": channel_id
    }

    # Update the JSON data
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=2)

json_path_server_channel_data =r"E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\game_server\server_channel_data.json"

def read_json_file(json_path):
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Fehler beim Laden der JSON-Datei {json_path}.")
        return None


data = read_json_file(json_path_server_channel_data)
for key in data:
    print(data[key]["server_address"])
    print(data[key]["channel_name_id"])
    print(data[key]["channel_stats_id"])



