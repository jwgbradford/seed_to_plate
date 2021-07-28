from local_data_handling import read_data

day, plant_key = '0', str(input('Do you want a pea plant(0) or a potato plant(1)\n>>> '))
weather_db = read_data('weather.json')
todays_weather = weather_db[day]

class Plant():
    def __init__(self, plant_key):
        self.get_attr(self.get_plant_data(plant_key))
        self.daily_growth_rate = self.final_height/self.days_to_harvest
    def get_plant_data(self, plant_key):
        plant_db = read_data('plant.json')
        return plant_db[plant_key]
    def get_attr(self, plant_model):
        for key in plant_model:
            setattr(self, key, plant_model[key])
    def grow(self):
        print(self.get_growth_from_temp())
    def get_growth_from_temp(self, growth_from_temp = 0):
        #protection = plants_modifers[plant_key][todays_weather['type']]
        if todays_weather['type'] == 'Snow':
            if self.snow_min_temp != '?':
                if todays_weather['temp'] < self.snow_min_temp:
                    growth_from_temp = 0
            else:
                growth_from_temp = 0
        else:
            if (todays_weather['temp'] <= self.max_temp) or (todays_weather['temp'] >= self.min_temp):
                if todays_weather['temp'] > self.ideal_temp:
                    growth_from_temp = 1 - ((todays_weather['temp'] - self.ideal_temp) / (self.max_temp - self.ideal_temp))
                elif todays_weather['temp'] < self.ideal_temp:
                    growth_from_temp = 1 - ((self.ideal_temp - todays_weather['temp']) / (self.ideal_temp - self.min_temp))
                else:
                    growth_from_temp = 1
            else: 
                growth_from_temp = 0
        return growth_from_temp
        

current_plants = []
current_plants.append(Plant(plant_key))
for plant in current_plants:
    plant.grow()