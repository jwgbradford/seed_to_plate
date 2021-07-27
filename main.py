from local_data_handling import read_data

day = '0' # keep everything on separate lines, it's easier to read for others
plant_key = str(input('Do you want a pea plant(0) or a potato plant(1)\n>>> '))
# I've moved the data handling (read / write) to a separate file
# this will make it easier when we get to client-server
plant_db = read_data('plant.json') 
weather_db = read_data('weather.json')

plant_model = plant_db[plant_key]
todays_weather = weather_db[day]

try:
    if todays_weather['type'] == 'Snow' and todays_weather['temp'] < plant_model['snow_min_temp']:
        print('plant_froze')
except:
    pass
print(plant_model)