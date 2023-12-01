"""
Use: - from util.__funktion__ import *

ChatGPT promt for docstrgs:

In copy code mode,

write me a .py docstr ("""""") with the content:
Args, Returns and Example Usage.
For Args and Returns create a list with "- ".
and for Example Usage create a list with ">>>  ".
Here is the code:


"""
import requests
import json
import os
from configparser import ConfigParser
import shutil
import time
import sys

import discord

def new_path(base_path, *additional_paths):
    """
    Combines paths based on a base and optional additional paths.
    
    Args:
        base_path (str): The base path.
        *additional_paths (str): Any number of additional paths.
        
    Returns:
        str: The combined and normalised path.
    """
    # Normalise the base path
    base_path = os.path.normpath(base_path)
    
    # Add all additional paths and create the combined path
    combined_path = os.path.join(base_path, *additional_paths)
    
    # Normalise and return the combined path
    return os.path.normpath(combined_path)


def read_config(config_dir, section, option, arg=None):
    """Reads a configuration file and returns the specified value as the desired data type.

Args:
- config_dir (str): The directory where the configuration file is located.
- section (str): The section of the configuration file where the option is located.
- option (str): The option to retrieve from the configuration file.
- arg (str, optional): The desired data type of the retrieved value. Can be "float", "int", or "tuple". Defaults to None.

Returns:
- If arg is not provided: the value of the specified option as a string.
- If arg is "float": the value of the specified option as a float.
- If arg is "int": the value of the specified option as an integer.
- If arg is "tuple": the value of the specified option as a tuple of integers.

Example Usage:
>>> read_config("config.ini", "database", "port")
'5432'

>>> read_config("config.ini", "database", "port", "int")
5432

>>> read_config("config.ini", "database", "credentials", "tuple")
(123456, 'password')
"""

    if arg == "float":
        config = ConfigParser()
        config.read(config_dir)
        load_config = (config[section][option])
        config_float = float(load_config)
        print(f"Config loaded: [ ({option})  = ({load_config}) ] conv to float")

        return config_int
    if arg == "int":
        config = ConfigParser()
        config.read(config_dir)
        load_config = (config[section][option])
        config_int = int(load_config)
        print(f"Config loaded: [ ({option})  = ({load_config}) ] conv to int")

        return config_int
    
    if arg == "tuple":
        config = ConfigParser()
        config.read(config_dir)
        load_config = (config[section][option])
        config_tuple = tuple(map(int, load_config.split(",")))
        print(f"Config loaded: [ ({option})  = ({load_config}) ] conv to tuple")

        return config_tuple
    
    else:
        config = ConfigParser()
        config.read(config_dir)
        load_config = (config[section][option])

        print(f"Config loaded: [ ({option})  = ({load_config}) ]")

        return load_config


def write_config(config_dir, section, Key, option):
    """
Args:
    - config_dir (str): The directory where the configuration file is located.
    - section (str): The section name in the configuration file.
    - Key (str): The key to update or add in the specified section.
    - option (str): The value to assign to the specified key.

Returns:
    - None

Example Usage:
    - Updating an existing key in a section of a configuration file
    >>>  write_config('config.ini', 'section1', 'key1', 'new_value')

    >>>  Adding a new key in a section of a configuration file
    >>>  write_config('config.ini', 'section2', 'key2', 'value2')
"""
    config = ConfigParser()
    # update existing value
    config.read(config_dir)
    try:
        config.add_section(section)
    except:
        pass
    option = str(option)
    config.set(section, Key, option)  # Updating existing entry
    with open(config_dir, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    print(
        f"\nChange settings -> {config_dir}\n[{section}]\n{Key}) = {option}\n")



def Folder_gen(Folder_Name, Folder_dir):
    """Creates a new folder if it does not already exist.

            Args:
            - folder_name (str): The name of the folder to be created.
            - folder_dir (str): The directory in which the folder is to be created.

            Returns:
            - str: The full path of the created folder.

            Example usage :
            >>> Folder_Name = "my_folder"
            >>> Folder_dir = "path/to/parent/directory"
            >>> created_folder_path = Folder_gen(Folder_Name, Folder_dir)
            >>> print("Created folder path:", created_folder_path)
    """

    print("Folder structure is checked and created if necessary...\n")
    folder = Folder_Name
    # Specifies desired file path
    #dir = "~/"+str(Folder_dir)+"/"+str(folder)
    full_path = Folder_dir + os.path.sep + Folder_Name
    # Adds file path with PC user name
    #full_path = os.path.expanduser(dir)
    # Checks file path for exsistance Ture/False
    if os.path.exists(full_path):
        print("Folder structure already exists")
        print("  ->   " + str(full_path))
    else:                                               # Creates folder if not available
        os.makedirs(full_path)
        print(f"The folder [{folder}] was created in the directory:\n  ->   {full_path}", "b")
        print("\n")
    return(os.path.normpath(full_path))


def Create_File(File_name, save_path, Inhalt):
    """Creates a new text file if it does not already exist and fills it with the specified content.

    Args:
    - File_name (str): The name of the text file.
    - save_path (str): The path where the text file should be saved.
    - Content (str): The content to be written to the text file.

    Returns:
    - str: The complete path of the created text file.

    Example usage:
    >>> file_name = "my_text_file.txt"
    >>> save_path = "/path/to/save/directory"
    >>> content = "This is the content of my text file."
    >>> created_file_path = Create_File(file_name, save_path, content)
    >>> print(created_file_path)
    '/path/to/save/directory/my_text_file.txt'
    """

    complete_Path_Text = save_path + os.path.sep + File_name
    if os.path.exists(complete_Path_Text):
        return complete_Path_Text
    else:
        # Create file
        file1 = open(complete_Path_Text, "w", encoding='utf-8')
        # toFile = input("Write what you want into the field")                   # File input def.
        # File is filled with input
        file1.write(f"{Inhalt}")
        file1.close()
        print(f"\nfile [{File_name}] is created...with conetnt:\{Inhalt}","b")
        return complete_Path_Text


def Read_File_Out(dir):
    """
    Reads the contents of a file located at the given directory path and returns it as a string.

    Args:
    - dir (str): The directory path of the file to be read.

    Returns:
    - content (str): The contents of the file as a string.

    Example usage:
    >>> file_path = "/path/to/file.txt"
    >>> content = Read_File_Out(file_path)
    >>> print(content)
    'This is the content of the file.'
    """
    with open(dir, 'r', encoding='utf-8') as f:
        content = f.read()

    return content


def copy_image(source_file, dest_file) -> None:
    """Copies an image file from the source path to the destination path.

    Args:
    - source_file (str): The path of the image file to be copied.
    - dest_file (str): The path where the image file should be copied to.

    Returns:
    - file (str) full path of the img

    Raises:
    - IOError: If an error occurs while copying the file.
    
    Example usage:
    >>> source_path = "/path/to/source/image.jpg"
    >>> dest_path = "/path/to/destination/image.jpg"
    >>> copy_image(source_path, dest_path)
    '/path/to/destination/image.jpg'
    """
    try:
        shutil.copy(source_file, dest_file)
        file = dest_file
        print(f"Image [{file}] successfully copied!", "b")
        return file
    except IOError as e:
        print(f"Error when copying the file: {e}", "r")


def File_name_with_time(FileName):
    """Generate a filename with a timestamp.

    Args:
    - FileName (str): The name of the file.

    Returns:
    - FullName (str): The full name of the file with a timestamp in the format of "FileName-DD_MM_YYYY-HH.MM".

    Example usage:
    >>> Datei_name_mit_Zeit("report")
    'report-04_04_2023-15.30'
    """
    Date = Date_Time=(time.strftime("%d_%m-%Y-%H.%M"))        # Generates date formater
    FullName = (FileName+"-"+(Date))                           # Generates file name
    return FullName


def TimeStemp():
    """
    Generates a timestamp string in the format of "dd_mm-yyyy_HH:MM:SS".

    Args:
        None

    Returns:
        A string representing the current date and time in the format "dd_mm-yyyy_HH:MM:SS".

    Example Usage:
        >>> TimeStemp()
        '04_04-2023_11:22:33'
    """
    TimeStemp = Date_Time=(time.strftime("%d_%m-%Y_%H:%M:%S"))
    return TimeStemp


def cheack_config(default_long_Str):
    """
    Generate a config file path in the 'cfg' directory of the current main file's directory.
    
    Args:
    - default_long_Str (str): A long string representing the default configuration
    
    Returns:
    - config_path (str): The absolute path to the generated config file
    
    Example Usage:
    >>> default_config = "This is the default configuration"
    >>> check_config(default_config)
    '/path/to/main_dir/cfg/config.ini'
    """
    main_file = sys.modules['__main__'].__file__
    main_dir = os.path.dirname(main_file)
    config_path =  Folder_gen("cfg", main_dir)
    config_path = Create_File("config.ini", config_path, default_long_Str)
    return config_path

if __name__ == "__funktion__":
    print("__function should not be executed when the file is imported as a module.\nThis was not the case!", "r")
else:
    cheack_config("""[Test]
    abc = 123""")

################################################################################################################################
#def spez.

def Discord_Activity(Text):
    """
    Creates a Discord Activity object with the specified text and type.

    Args:
        Text (str): The text to display as the activity.

    Returns:
        - Activity (discord.Activity): A Discord Activity object with the specified text and type.

    Example Usage:
        >>> import discord
        >>> activity = Discord_Activity("Watching a movie")
        >>> client = discord.Client(activity=activity)
    """
    #Activity = discord.Client(activity=discord.Game(name='my game'))
    Activity = discord.Activity(name=Text, type=discord.ActivityType.watching)
    return Activity


def add_new_channel_data(user_name, user_id, channel_id, json_path):
    # Read in the existing JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Add the new data
    new_channel_data = {
        "user_id": {
            "owner_name":user_name,
            "channel_id": channel_id,
            "channel_msg_id": "",
            "admin": [user_id],
            "limit": "0",
            "banned": "",
            "hide": False,
            "stay": False
        }
    }

    # Add the new data to the existing data object
    data[user_id] = new_channel_data["user_id"]

    # Write the updated data back to the JSON file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=2)


def is_user_in(user_id, json_path):
    if user_id == int:
        user_id = str(user_id)
    # Read in the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)
    return str(user_id) in data.keys()


def is_channel_id_in(channel_id, json_path):
    if channel_id == str:
        channel_id = int(channel_id)
    # Read in the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Check whether the channel_id is present
    for user_id, user_data in data.items():
        if "channel_id" in user_data and user_data["channel_id"] == channel_id:
            return True

    # If the channel_id was not found
    return False


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


def get_channel_id_from(owner_id, json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for channel_id, channel_data in data.items():
        if channel_id == str(owner_id):
            return channel_data.get("channel_id")
    return None  # If the owner_id is not found


def is_he_channel_admin(user_id, channel_id, json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for key, value in data.items():
        if "channel_id" in value and value["channel_id"] == channel_id:
            if "admin" in value and user_id in value["admin"]:
                return True

    return False


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
    

def read_json_file(json_path):
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Fehler beim Laden der JSON-Datei {json_path}.")
        return None


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



def fill_item_in_channel(channel_id, item, fill, json_path):
    # Load the JSON from the file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Iterate through the keys of the outer object
    for key, value in data.items():
        # Check if the channel_id is present in the inner object
        if "channel_id" in value and value["channel_id"] == channel_id:
            # Update the element in the found object
            value[item] = fill

            # Save the updated data back to the file
            with open(json_path, 'w') as file:
                json.dump(data, file, indent=2)
            print(f"Successfully updated {item} for channel {channel_id}.")
            return  # Exit the function after the update is done

    # If the function reaches here, the channel was not found
    print(f"Channel {channel_id} not found.")


def discord_time_convert(time):
    """
    Converts a Unix timestamp to Discord time format.

    Args:
        time (int): A Unix timestamp to convert to Discord time format.



    Returns:
        - discord_time (str): A string representing the input timestamp in Discord time format.

    Example Usage:
        >>> timestamp = 1617123999
        >>> discord_time = discord_time_convert(timestamp)
        >>> print(discord_time)
        '<t:1617123999:R>'
            1678369942473.0
    """
    time = int(str(time)[:10])
    discord_time = (f"<t:{time}:R>")
    return discord_time


def find_user_id_occurrences(data_set, target_user_id):
    matching_keys = []

    for key, data in data_set.items():
        if data["user_id"] == target_user_id:
            matching_keys.append(key)

    return matching_keys


def add_new_ticket_data(json_path, key, type, user_name, user_id, ticket_channel_id, ticket_role_id, time_stemp, ticket_status):
    # Load existing data from the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Check if the key already exists in the data
    if key in data:
        print(f"Entry with key {key} already exists.")
    else:
        # Add a new entry
        data[key] = {
            "type": type,
            "user_name": user_name,
            "user_id": user_id,
            "ticket_channel_id": ticket_channel_id,
            "voice_channel_id": "",
            "ticket_role_id": ticket_role_id,
            "unix_timestemp": time_stemp,
            "ticket_status": ticket_status
        }

        # Write the updated data back to the JSON file
        with open(json_path, 'w') as file:
            json.dump(data, file, indent=2)


def support_entry_in_data(json_path, login_unix_time, user_name, user_id):
    # Lade das vorhandene JSON
    with open(json_path, 'r') as file:
        datensatz = json.load(file)

    datensatz[login_unix_time] = {
        "user_name": user_name,
        "user_id": user_id,
        "claimed_tickets": [],
        "check_out": ""
    }

    with open(json_path, 'w') as file:
        json.dump(datensatz, file, indent=2, separators=(',', ':'))


def support_update_check_out(data=None, json_path=None, user_id=None, timestamp=None):
    # Check if 'data' is provided directly, otherwise load the JSON file
    if data is None:
        with open(json_path, 'r') as file:
            data = json.load(file)

    matching_entries = [key for key, entry in data.items() if str(user_id) == str(entry.get('user_id'))]

    if matching_entries:
        latest_entry_key = max(matching_entries, key=lambda x: float(x))
        latest_entry = data[latest_entry_key]

        latest_entry['check_out'] = timestamp

        # Save the updated data back to the file
        if json_path is not None:
            with open(json_path, 'w') as file:
                json.dump(data, file, indent=2)
        else:
            print("Warning: 'json_path' not provided. Data was not saved to a file.")

    else:
        print(f"User with the ID {user_id} was not found.")


def find_open_tickets_keys(json_path=None, data=None):
    if data is None:
        with open(json_path, 'r') as file:
            data = json.load(file)

    open_tickets = []
    for key, value in data.items():

        if "ticket_status" in value and (value["ticket_status"] == "open" or value["ticket_status"] == "claimed" or value["ticket_status"] =="voice support"):
            open_tickets.append(key)

    return open_tickets


def support_dashboard_text(json_path_ticket, interaction_guild_members, aktiv_support_team_role, support_team_role):
    """
    interaction_guild_members = interaction.guild.members
    """
    aktive_supporter_str = ""
    users_with_aktiv_support_team_role = [member.id for member in interaction_guild_members if aktiv_support_team_role in member.roles]

    for id in users_with_aktiv_support_team_role:
        aktive_supporter_str = aktive_supporter_str + f"<@{id}>\n"

    users_with_support_team_role = [member.id for member in interaction_guild_members if support_team_role in member.roles]
    pasive_support_users = users_with_support_team_role
    for id in users_with_aktiv_support_team_role:
        pasive_support_users.remove(id)

    pasiv_supporter_str = ""
    for id in pasive_support_users:
        pasiv_supporter_str = pasiv_supporter_str + f"<@{id}>\n"

    data = read_json_file(json_path_ticket)
    open_tickets_key = find_open_tickets_keys(data=data)


    open_ticket_str = ""
    for key in open_tickets_key:
        ticket_status = (data[key]["ticket_status"])
        ticket_channel_id = (data[key]["ticket_channel_id"])
        user_id = (data[key]["user_id"])
        type = (data[key]["type"])
        unix_timestemp = (data[key]["unix_timestemp"])
        discord_time = discord_time_convert(unix_timestemp)
        open_ticket_str = open_ticket_str + f"> **{ticket_status}** **-** <#{ticket_channel_id}> **-** <@{user_id}> **-** **{type}** **-** {discord_time}\n\n"

    text = f"""**Support Check In**
    _Check In as active and receive notifications for open tickets._
    
    **Support Check Out**
    _Check Out as active and do not receive notifications for open tickets._
    
    **Aktive  Supporter:**
    {aktive_supporter_str}
    **Passive Supporter:**
    {pasiv_supporter_str}
    
    **Open Tickets:**
    {open_ticket_str}

    _last Dashboard update_ {discord_time_convert(time.time())}
"""
    return text


def find_key_by_user_id(json_data, target_user_id):
    for key, value in json_data.items():
        if "user_id" in value and value["user_id"] == target_user_id:
            return key
    return None


def is_user_id_in_data(json_data, target_user_id):
    for key, value in json_data.items():
        if "user_id" in value and value["user_id"] == target_user_id:
            return True
    return False


def update_json(json_path, key, target_item, new_value, loaded_data=None):
    if loaded_data is None:
        with open(json_path, 'r') as file:
            json_data = json.load(file)
    else:
        json_data = loaded_data

    if key in json_data:
        if target_item in json_data[key]:
            json_data[key][target_item] = new_value
            print(f"update -> json_data[{key}][{target_item}] = {new_value}")
        else:
            print(f'The element {target_item} was not found in the key {key}')
    else:
        print(f'The key {key} was not found in the JSON')
        
    with open(json_path, 'w') as file:
        json.dump(json_data, file, indent=2)


def find_last_entry_key(json_data, user_id):
    # Lade den JSON-Datensatz
    # Durchsuche den Datensatz rückwärts nach der angegebenen user_id
    for key in reversed(sorted(json_data.keys())):
        entry = json_data[key]
        if entry["user_id"] == user_id:
            # Gib den Schlüssel (key) und den Eintrag zurück
            return key

    # Gib None zurück, wenn die user_id nicht gefunden wurde
    return None, None


def add_tickt_to_support_data(json_path, json_data, key, ticket_num):
    if key in json_data:
        json_data[key]["claimed_tickets"].append(ticket_num)

        try:
            with open(json_path, 'w') as file:
                json.dump(json_data, file, indent=2)
            print(f"Ticket {ticket_num} was successfully added.")
        except IOError as e:
            print(f"Error when writing the file {json_path}: {e}")
    else:
        print(f"The specified key '{key}' was not found in the JSON data set.")


def find_user_ids_by_ticket(json_data, ticket_num):
    user_ids = []

    for timestamp, data in json_data.items():
        claimed_tickets = data.get("claimed_tickets", [])

        if ticket_num in claimed_tickets:
            user_ids.append(data["user_id"])

    return user_ids


def find_key_by_ticket_channel(ticket_data, target_ticket_channel_id):
    for key, value in ticket_data.items():
        if "ticket_channel_id" in value and value["ticket_channel_id"] == target_ticket_channel_id:
            return key
    return None



def get_server_data(api_key, filter_param):
    url = "https://api.steampowered.com/IGameServersService/GetServerList/v1/"
    params = {
        'key': api_key,
        'filter': f"addr\\{filter_param}"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        data = response.json()
        time.sleep(1.5)
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
    

def add_server_data(json_path, server_address, server_name, channel_name_id, channel_stats_id, server_msg_id):
    # Read the existing JSON data
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Find the highest existing key
    max_key = max(map(int, data.keys())) if data else 0

    # Create a new key (one higher than the highest existing key)
    new_key = str(max_key + 1)

    # Add the new entry
    data[new_key] = {
        "server_name": server_name,
        "server_address": server_address,
        "channel_name_id": channel_name_id,
        "channel_stats_id" : channel_stats_id
    }

    # Update the JSON data
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=2)


def check_ip_in_data(json_path, ip):
    # Laden Sie das JSON-Dataset aus der angegebenen Datei
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Durchsuchen des Datasets nach der angegebenen IP-Adresse
    for key, server_info in data.items():
        if server_info["server_address"] == ip:
            return key  # Rückgabe des Schlüssels, wenn die IP gefunden wurde

    # Rückgabe von False, wenn die IP nicht gefunden wurde
    return False


def get_server_addresses(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    server_addresses = [entry["server_address"] for entry in data.values()]
    return server_addresses


def delete_entry(json_path, key):
    with open(json_path, 'r') as file:
        data = json.load(file)

    if key in data:
        del data[key]
        with open(json_path, 'w') as file:
            json.dump(data, file, indent=2)
        print(f"Entry with the key '{key}' was successfully deleted.")

    else:
        print(f"Entry with the key '{key}' was not found.")