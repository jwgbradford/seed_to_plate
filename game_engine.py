from local_data_handling import read_data

class Plant():
    def __init__(self, plant_key):
        self.set_attributes(self.get_plant_data(plant_key))
        self.daily_growth_rate = self.final_height/self.days_to_harvest
        self.my_height, self.recovery_days = 0, 0

    def get_plant_data(self, plant_key):
        plant_db = read_data('plant.json')
        return plant_db[plant_key]

    def set_attributes(self, plant_model):
        for key in plant_model:
            setattr(self, key, plant_model[key])

    def grow(self, weather_today):
        if self.recovery_days <= 0:
            temperature_modifier = self.growth_modifier_temperature(weather_today['temp'], weather_today['type'])
            growth_today = self.daily_growth_rate * temperature_modifier
            self.my_height += growth_today
        else:
            self.recovery_days -= 1

    def growth_modifier_temperature(self, temp, modifier):
        #protection = plants_modifers[plant_key][todays_weather['type']]
        if temp > self.ideal_temp:
            growth_from_temp = 1 - ((temp - self.ideal_temp) / (self.max_temp - self.ideal_temp))
        elif temp < self.ideal_temp:
            if modifier == "Snow":
                growth_from_temp = 1 - ((self.ideal_temp - temp) / (self.ideal_temp - self.snow_min_temp))
            else:
                growth_from_temp = 1 - ((self.ideal_temp - temp) / (self.ideal_temp - self.min_temp))
        else:
            growth_from_temp = 1
        # we don't want our plant to 'ungrow'
        if growth_from_temp < 0:
            growth_from_temp = 0
            self.recovery_days += 1
        return growth_from_temp

if __name__ == "__main__":
    weather_history, current_plants = read_data('weather.json'), []
    current_plants.append(Plant(str(input('Do you want a pea plant(0) or a potato plant(1)\n>>> '))))
    for today in weather_history:
        for plant in current_plants:
            plant.grow(weather_history[today])
            print(plant.my_height)
            print('rd: ', plant.recovery_days)