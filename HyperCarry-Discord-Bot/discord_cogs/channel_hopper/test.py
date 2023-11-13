import json

json_path = "E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\channel_hopper\channel_data.json"

import json

def add_new_channel_data(name, channel_id, json_path):
    # Read in the existing JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Add the new data
    new_channel_data = {
        "user_id": {
            "channel_id": channel_id,
            "admin": name,
            "limit": "0",
            "banned": "",
            "hide": False,
            "status": ""
        }
    }

    # Add the new data to the existing data object
    data[name] = new_channel_data["user_id"]

    # Write the updated data back to the JSON file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=2)

# Beispielaufruf der Funktion

#add_new_channel_data(22,13 ,json_path)



import json

def is_user_in(user_id, json_path):
    if user_id == int:
        user_id = str(user_id)
    # Read in the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)
    return str(user_id) in data.keys()


# Example call of the function
# result = is_user_in("2222", json_path)
# print(result)


import json

def is_channel_id_in(channel_id, json_path):
    if channel_id == str:
        channel_id = int(channel_id)
    # Lese die JSON-Datei ein
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Überprüfe, ob die channel_id vorhanden ist
    for user_id, user_data in data.items():
        if "channel_id" in user_data and user_data["channel_id"] == channel_id:
            return True

    # Wenn die channel_id nicht gefunden wurde
    return False

# Beispielaufruf der Funktion
# result = is_channel_id_in(123456, json_path)
# print(result)


import json

def delete_data_with_channel_id(channel_id, json_path):
    # Read in the existing JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Check if the channel_id is present
    for user_id, user_data in list(data.items()):
        if "channel_id" in user_data and user_data["channel_id"] == channel_id:
            # Delete the parent data object
            del data[user_id]

    # Write the updated data back to the JSON file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=2)

# Example function call
#delete_data_with_channel_id(12, json_path)



def get_channel_id_from(owner_id, json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for channel_id, channel_data in data.items():
        if channel_id == str(owner_id):
            return channel_data.get("channel_id")
    return None  # If the owner_id is not found


#print(is_user_in("189025602236448778", json_path))

"""
        if is_user_in(user_id, json_path) == True:
            channel_id = get_channel_id_from(user_id, json_path)
            channel = bot.get_channel(channel_id)
            user.move_to(channel)

        embed = discord.Embed(title=py_name, color=0xff80ff)
        embed.set_author(name="created by Napo_II",
                         url="https://github.com/NapoII/HyperCarry-Disocrd-Bot")
        embed.set_thumbnail(url="https://i.imgur.com/hcVwvZF.png")
        embed.add_field(name="Version", value=v, inline=True)
        embed.add_field(
            name="python", value=f"{python_version()}", inline=True)
        embed.add_field(name="github", value="https://github.com/NapoII/HyperCarry-Discord-Bot", inline=False)
        await channel.send(embed=embed)

        embed.add_field(name="Feld 1", value="Wert 1", inline=False)
        embed.add_field(name="Feld 2", value="Wert 2", inline=True)

        # Sende das Embed als private Nachricht an den Benutzer
        await user.send(embed=embed)
    """
    

import json

def is_he_channel_admin(user_id, channel_id, json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for key, value in data.items():
        if "channel_id" in value and value["channel_id"] == channel_id:
            if "admin" in value and user_id in value["admin"]:
                return True

    return False

# x = is_he_channel_admin(123, 11728707564142797223, json_path)

def get_channel_id_for_user_in_admin(user_id, json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for key, value in data.items():
        if "admin" in value:
            if user_id == value["admin"] or (isinstance(value["admin"], list) and user_id in value["admin"]):
                return value["channel_id"]

    return False


def get_list_for_all_admin_server_from_user(user_id, json_path):
    channel_ids = []

    with open(json_path, 'r') as file:
        data = json.load(file)

    for key, value in data.items():
        if "admin" in value:
            if user_id == value["admin"] or (isinstance(value["admin"], list) and user_id in value["admin"]):
                channel_ids.append(value["channel_id"])

    return channel_ids


x = get_list_for_all_admin_server_from_user(222, json_path)

#print(x)

def get_stay_status(target_channel_id, json_path):
    # Read in the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Search the data structure for the subcategory with the target channel ID
    for main_key, subcategory_data in data.items():
        if "channel_id" in subcategory_data and subcategory_data["channel_id"] == target_channel_id:
            stay_value = data.get(main_key, {}).get("stay")
            return stay_value
    
    return None
    
#x = get_main_key(json_path, 1172908485898420268)
#print(x)


def switch_stay_status(target_channel_id, json_path):
    # Read in the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Search the data structure for the subcategory with the target channel ID
    for main_key, subcategory_data in data.items():
        if "channel_id" in subcategory_data and subcategory_data["channel_id"] == target_channel_id:
            # Toggle the "stay" value
            subcategory_data["stay"] = not subcategory_data.get("stay", True)

            # Write the updated data back to the JSON file
            with open(json_path, 'w') as write_file:
                json.dump(data, write_file, indent=2)

            # Return the updated "stay" value
            return subcategory_data["stay"]

    # Return None if the target channel ID is not found
    return None

#x = switch_stay_status(1172908485898420268, json_path)

def get_admin_list(channel_id, json_path):
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)

        for key, value in data.items():
            if "channel_id" in value and value["channel_id"] == channel_id:
                return value.get("admin", [])
        
        print(f"Channel mit ID {channel_id} nicht gefunden.")
        return []

    except FileNotFoundError:
        print(f"Datei {json_path} nicht gefunden.")
        return []


# x = get_admin_list(1172908485898420268, json_path)

def get_item_from_channel(item, target_channel_id, json_path):
    # Read in the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Search the data structure for the subcategory with the target channel ID
    for main_key, subcategory_data in data.items():
        if "channel_id" in subcategory_data and subcategory_data["channel_id"] == target_channel_id:
            value = data.get(main_key, {}).get(f"{item}")
            return value
    
    return None


"""result = get_item_from_channel("stay", 1172937156554129569, json_path)
print(resul"""


def get_item_from_channel(item, target_channel_id, json_input):
    # If json_input is a file path, read the JSON file
    if isinstance(json_input, str):
        with open(json_input, 'r') as file:
            data = json.load(file)
    # If json_input is already a JSON object, use it directly
    elif isinstance(json_input, dict):
        data = json_input
    else:
        raise ValueError("Invalid json_input type. Please provide either a file path (str) or a JSON object (dict).")

    # Search the data structure for the subcategory with the target channel ID
    for main_key, subcategory_data in data.items():
        if "channel_id" in subcategory_data and subcategory_data["channel_id"] == target_channel_id:
            value = data.get(main_key, {}).get(f"{item}")
            return value
    
    return None


def read_json_file(json_path):
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Fehler beim Laden der JSON-Datei {json_path}.")
        return None




data = read_json_file(json_path)
x = get_item_from_channel("stay", 1172945469962469457, data)
y = get_item_from_channel("stay", 1172945469962469457, json_path)
#print(x,y)


def find_main_key(json_path, target_channel_id):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for main_key, channel_data in data.items():
        if "channel_id" in channel_data and channel_data["channel_id"] == target_channel_id:
            return main_key

    return None


#print (find_main_key(json_path, 1172960279525609512))


data= read_json_file(json_path)

def find_main_key(target_channel_id, data_or_path):
    if isinstance(data_or_path, str):  # If it's a file path, load the data.
        with open(data_or_path, 'r') as file:
            data = json.load(file)
    elif isinstance(data_or_path, dict):  # If it's already loaded data, use it directly.
        data = data_or_path
    else:
        raise ValueError("Invalid type for data_or_path. Expected either a file path (str) or already loaded data (dict).")

    for main_key, channel_data in data.items():
        if "channel_id" in channel_data and channel_data["channel_id"] == target_channel_id:
            return main_key

    return None


x = find_main_key(1173008981627764821, data)
print(x)