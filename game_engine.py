from local_data_handling import read_data

day, plant_key = '0', str(input('Do you want a pea plant(0) or a potato plant(1)\n>>> '))
weather_db = read_data('plant.json'), read_data('weather.json')
todays_weather = weather_db[day]

class Plant():
    def __init__(self, plant_key):
        self.health = self.get_health()
        plant_model = self.get_plant_data(plant_key)
        self.get_attr(plant_model)
        self.growth_end = 30,000

    def get_plant_data(self, plant_key):
        plant_db = read_data('plant.json')
        return plant_db[plant_key]

    def get_attr(self, plant_model):
        for key in plant_model:
            setattr(self, key, plant_model[key])

    def grow(self):
        if self.growth_end != 0:
            self.growth_end -= self.health
        self.current_height = self.height-(self.growth_end/10,000)

    def get_growth_from_temp(self, growth_from_temp = 0):
        #protection = plants_modifers[plant_key][todays_weather['type']]
        if todays_weather['type'] == 'Snow':
            if self.snow_min_temp != '?':
                if todays_weather['temp'] < self.snow_min_temp:
                    growth_from_temp = 0
            else:
                growth_from_temp = 0
        else:
            if (todays_weather['temp']<=self.max_temp) or (todays_weather['temp']>=self.min_temp):
                if todays_weather['temp']>=self.ideal_temp:
                    growth_from_temp = 100-(self.max_temp*todays_weather['temp'])
                else:
                    growth_from_temp = 100-(self.min_temp*todays_weather['temp'])
            else: growth_from_temp = 0
            
        return growth_from_temp
        

current_plants = []
current_plants.append(Plant(plant_key))