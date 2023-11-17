
import json
json_path = r"E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\ticket_system\ticket_data.json"


def read_json_file(json_path):
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Fehler beim Laden der JSON-Datei {json_path}.")
        return None






def read_json_file(json_path):
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Fehler beim Laden der JSON-Datei {json_path}.")
        return None



#data = read_json_file(json_path)

def find_user_id_occurrences(data_set, target_user_id):
    matching_keys = []

    for key, data in data_set.items():
        if data["user_id"] == target_user_id:
            matching_keys.append(key)

    return matching_keys

#x = find_user_id_occurrences(data, 11)

def add_new_ticket_data(json_path, key, user_name, user_id, channel_msg_id):
    # Load existing data from the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Check if the key already exists in the data
    if key in data:
        print(f"Entry with key {key} already exists.")
    else:
        # Add a new entry
        data[key] = {
            "user_name": user_name,
            "user_id": user_id,
            "channel_msg_id": channel_msg_id
        }

        # Write the updated data back to the JSON file
        with open(json_path, 'w') as file:
            json.dump(data, file, indent=2)

        print(f"New ticket with key {key} has been added to the JSON file.")


json_path = r"E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\ticket_system\support_team_data.json"

def support_entry_in_data(json_path, login_unix_time, user_name):
    # Lade das vorhandene JSON
    with open(json_path, 'r') as file:
        datensatz = json.load(file)

    datensatz[login_unix_time] = {
        "user_name": user_name,
        "claimed_ticks": "",
        "check_out": ""
    }

    with open(json_path, 'w') as file:
        json.dump(datensatz, file, indent=2, separators=(',', ':'))


# Beispielaufruf der Funktion
neue_login_unix_time = 444
neuer_user_name = "wixxer"

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

        if "ticket_status" in value and value["ticket_status"] == "open":
            open_tickets.append(key)

    return open_tickets

json_path = r"E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\ticket_system\ticket_data.json"
data = read_json_file(json_path)



data = read_json_file(json_path)
open_tickets_key = find_open_tickets_keys( data=data)


def find_key_by_user_id(json_data, target_user_id):
    for key, value in json_data.items():
        if "user_id" in value and value["user_id"] == target_user_id:
            return key
    return None

x = find_key_by_user_id(data, 189025602236448778)

def is_user_id_in_data(json_data, target_user_id):
    for key, value in json_data.items():
        if "user_id" in value and value["user_id"] == target_user_id:
            return True
    return False

x = is_user_id_in_data(data, 189025602236448778)


def update_json(json_path, key, target_item, new_value):
    # Lese JSON-Datei ein
    with open(json_path, 'r') as file:
        json_data = json.load(file)

    # Überprüfe, ob der angegebene Schlüssel im JSON vorhanden ist
    if key in json_data:
        # Überprüfe, ob das gewünschte Ziel-Element im angegebenen Schlüssel vorhanden ist
        if target_item in json_data[key]:
            # Ändere den Wert des target_item auf new_value
            json_data[key][target_item] = new_value
        else:
            print(f'Das Element {target_item} wurde nicht im Schlüssel {key} gefunden.')
    else:
        print(f'Der Schlüssel {key} wurde nicht im JSON gefunden.')

    # Speichere die aktualisierten Daten zurück in die JSON-Datei
    with open(json_path, 'w') as file:
        json.dump(json_data, file, indent=2)

def read_json_file(json_path):
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Fehler beim Laden der JSON-Datei {json_path}.")
        return None

json_path = r"E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\ticket_system\support_team_data.json"

def read_json_file(json_path):
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Fehler beim Laden der JSON-Datei {json_path}.")
        return None

json_data = read_json_file(json_path)


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


support_team_data_path = r"E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\ticket_system\support_team_data.json"
ticket_data_path = r"E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\ticket_system\ticket_data.json"

support_team_data = read_json_file(support_team_data_path)
ticket_data = read_json_file(ticket_data_path)


key = find_last_entry_key(json_data, 314094103459528705)

#print(x)


def update_json_data(json_path, json_data, key, ticket_num):
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

#update_json_data(json_path, json_data, key, 124)

def find_user_ids_by_ticket(json_data, ticket_num):
    user_ids = []

    for timestamp, data in json_data.items():
        claimed_tickets = data.get("claimed_tickets", [])

        if ticket_num in claimed_tickets:
            user_ids.append(data["user_id"])

    return user_ids

x = find_user_ids_by_ticket(support_team_data, 1)
# print(x)


def find_key_by_ticket_channel(ticket_data, target_ticket_channel_id):
    for key, value in ticket_data.items():
        if "ticket_channel_id" in value and value["ticket_channel_id"] == target_ticket_channel_id:
            return key
    return None

x = find_key_by_ticket_channel(ticket_data, 1174802850354831512)


def update_json(json_path, key, target_item, new_value, loaded_data=None):
    if loaded_data is None:
        with open(json_path, 'r') as file:
            json_data = json.load(file)
    else:
        json_data = loaded_data

    if key in json_data:
        if target_item in json_data[key]:
            json_data[key][target_item] = new_value
        else:
            print(f'The element {target_item} was not found in the key {key}').
    else:
        print(f'The key {key} was not found in the JSON')


    with open(json_path, 'w') as file:
        json.dump(json_data, file, indent=2)


json_path = r"E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\ticket_system\ticket_data.json"
data = read_json_file(json_path)

update_json(json_path, "1", "ticket_status", "test", loaded_data=data)