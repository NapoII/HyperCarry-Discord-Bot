
import json
import time



# Beispielaufruf:
dateipfad = r'E:\Pr0grame\My_ Pyhton\work_in_progress\HyperCarry-Discord-Bot\HyperCarry-Discord-Bot\discord_cogs\ticket_system\ticket_data.json'


def update_ticket_json_values(json_path, key, ticket_channel_id, ticket_role_id, ticket_status):
    # Read the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)
    print("333333333333")

    data[key]["ticket_channel_id"] = ticket_channel_id
    data[key]["ticket_role_id"] = ticket_role_id
    data[key]["ticket_status"] = ticket_status
    data[key]["unix_timestemp"] = time.time()
    
    # Write the updated data back to the JSON file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=2)

        

update_ticket_json_values(dateipfad, "11", 1, 2, 3)