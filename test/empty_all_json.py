import json
import os

def overwrite_json(file_path):
    data = {}
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

def main():
    # List of JSON file paths
    json_files = []

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