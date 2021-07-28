import json, random

def write_data(dict_to_save, file_name):
    with open(file_name, 'w') as file:
        json.dump(dict_to_save, file, indent=2)
    file.close

def read_data(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    file.closed
    return data