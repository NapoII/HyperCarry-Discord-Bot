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
        print(f"Config loaded: [ ({option})  = ({config_float}) ] conv to float", "g")

        return config_int
    if arg == "int":
        config = ConfigParser()
        config.read(config_dir)
        load_config = (config[section][option])
        config_int = int(load_config)
        print(f"Config loaded: [ ({option})  = ({config_tuple}) ] conv to int", "g")

        return config_int
    
    if arg == "tuple":
        config = ConfigParser()
        config.read(config_dir)
        load_config = (config[section][option])
        config_tuple = tuple(map(int, load_config.split(",")))
        print(f"Config loaded: [ ({option})  = ({config_tuple}) ] conv to tuple", "g")

        return config_tuple
    
    else:
        config = ConfigParser()
        config.read(config_dir)
        load_config = (config[section][option])

        print(f"Config loaded: [ ({option})  = ({load_config}) ]", "g")

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


def find_main_key(json_path, target_channel_id):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for main_key, channel_data in data.items():
        if "channel_id" in channel_data and channel_data["channel_id"] == target_channel_id:
            return main_key

    return None