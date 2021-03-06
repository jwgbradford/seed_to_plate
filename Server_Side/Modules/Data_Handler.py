import json

plant_dict = {
    'Fruit': {
        0: {
            'name': 'pea', 
            'snow_min_temp': -15, 
            'min_temp': -2, 
            'ideal_temp': 10, 
            'max_temp': 21, 
            'ideal_sunlight': 5, 
            'ideal_branches': 74.8, 
            'final_height': 0.9114, 
            'days_to_flower': 91, 
            'days_to_fruit': 94, 
            'days_to_harvest': 142, 
            'ideal_water': 0.114
        },
        1: {
            'name': 'tomato', 
            'snow_min_temp': '?', 
            'min_temp': 16, 
            'ideal_temp': 21, 
            'max_temp': 27, 
            'ideal_sunlight': 8, 
            'ideal_branches': 100, 
            'final_height': 1.8, 
            'days_to_flower': 45, 
            'days_to_fruit': 80, 
            'days_to_harvest': 120, 
            'ideal_water': 0.25
        }
    },
    'Tuber': {
        0: {
            'name': 'potato', 
            'snow_min_temp': '?', 
            'min_temp': 10, 
            'ideal_temp': 20, 
            'max_temp': 35, 
            'ideal_sunlight': 8, 
            'ideal_branches': 7, 
            'final_height': 1,
            'days_to_flower': 56, 
            'days_to_fruit': 70, 
            'days_to_harvest': 84,  
            'ideal_water': 0.1311,
            'ideal_tubers': 10
        }
    }
}

def write_data(dict_to_save, file_name):
    with open(file_name, 'w+') as file:
        json.dump(dict_to_save, file, indent=4)
    file.close

def read_data(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    file.closed
    return data

write_data(plant_dict, 'plant.json')
