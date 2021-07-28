from local_data_handling import write_data, random

weather_dict = {
    day: {'type': random.choice(['Snow', 'Normal']), 'temp': round(random.uniform(-8, 18), 2), 'sun': round(random.uniform(0,18), 2), 'rainfall': random.uniform(0, 2)} for day in range(0, 30)
}

plant_dict = {
    0: {'name': 'pea', 'snow_min_temp': -15, 'min_temp': -2, 'ideal_temp': 10, 'max_temp': 21, 'ideal_sunlight': 5, 'ideal_branches': 74.8, 'final_height': 0.9114, 'days_to_flower': 91, 'days_to_fruit': 94, 'days_to_harvest': 142, 'hydration_decay': 4.76, 'ideal_water': 0.014},
    1: {'name': 'potato', 'snow_min_temp': '?', 'min_temp': 10, 'ideal_temp': 20, 'max-temp': 35, 'ideal_sunlight': 8, 'ideal_branches': 7, 'final_height': 1,'days_to_flower': 70, 'days_to_fruit': 120, 'days_to_harvest': 75, 'hydration_decay': 4.76, 'ideal_water': 0.1311}

}

'''modifers = {
    plant_id: {weather_type: protection}
        }
'''
write_data(weather_dict, 'weather.json')
write_data(plant_dict, 'plant.json')