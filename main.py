import json

day, plants_key = '0', str(input('Do you want a pea plant(0) or a potato plant(1)\n>>> '))
plant_db, weather_db = json.load(open('Plant.json', 'r')), json.load(open('Weather.json', 'r'))

plant_model, todays_weather = plant_db[plants_key], weather_db[day]

try:
    if todays_weather['type'] == 'Snow' and todays_weather['temp'] < plant_model['snow_min_temp']:
        print('plant_froze')




print(plant_model)