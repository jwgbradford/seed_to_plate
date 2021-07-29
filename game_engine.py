from local_data_handling import read_data

class Plant():
    def __init__(self, plant_key):
        self.set_attributes(self.get_plant_data(plant_key))
        self.daily_growth_rate = self.final_height/self.days_to_harvest
        self.my_height, self.stored_water = 0, 0
        self.sun_recovery_day, self.water_recovery_day, self.temp_recovery_day = 0, 0, 0

    def get_plant_data(self, plant_key):
        plant_db = read_data('plant.json')
        return plant_db[plant_key]

    def set_attributes(self, plant_model):
        for key in plant_model:
            setattr(self, key, plant_model[key])

    def grow(self, weather_today):
        sunlight_modifier = self.growth_modifier_sunlight(weather_today['sun'])
        hydration_modifier = self.growth_modifier_hydration(weather_today['rainfall'])
        temperature_modifier = self.growth_modifier_temperature(weather_today['temp'], weather_today['type'])
        growth_today = self.daily_growth_rate * temperature_modifier * hydration_modifier * sunlight_modifier
        self.my_height += growth_today

    def growth_modifier_temperature(self, temp, modifier):
        if temp > self.ideal_temp:
            growth_from_temp = 1 - (temp - self.ideal_temp) / (self.max_temp - self.ideal_temp)
        elif temp < self.ideal_temp:
            if (modifier == "Snow") and (self.snow_min_temp != "?"):
                growth_from_temp = 1 - (self.ideal_temp - temp) / (self.ideal_temp - self.snow_min_temp)
            else:
                growth_from_temp = 1 - (self.ideal_temp - temp) / (self.ideal_temp - self.min_temp)
        if (self.temp_recovery_day > 0) and (growth_from_temp > 0):
            self.temp_recovery_day -= 1
            growth_from_temp = 0
        elif growth_from_temp < 0:
            growth_from_temp = 0
            self.temp_recovery_day += 1
        return growth_from_temp

    def growth_modifier_hydration(self, rainfall):
        self.stored_water += rainfall # put rainfall in soil
        growth_from_hydration = 0 
        # if there is more water in the soil than too 2 weeks worth of the plan't water consumption
        # or if there is no water in the soil
        if (self.stored_water > 14 * self.ideal_water) or (self.stored_water == 0):
            self.water_recovery_day += 1 
        # if we would grow but the plant need to recover take of a day to recover and don't grow
        elif (self.water_recovery_day > 0) and (self.stored_water > self.ideal_water):
            self.water_recovery_day -= 1
            self.stored_water -= self.ideal_water
        # if we would grow and we don't need to recover see how much we would grow from the water
        elif self.water_recovery_day == 0:
            if self.stored_water < self.ideal_water:
                growth_from_hydration = 1-(self.ideal_water - rainfall) / self.ideal_water
                self.stored_water -= rainfall
            else:
                growth_from_hydration = 1
                self.stored_water -= self.ideal_water
        return growth_from_hydration

    def growth_modifier_sunlight(self, sunlight):
        #get how much plant grows
        if sunlight == self.ideal_sunlight: 
            growth_from_sunlight = 1
        else:
            growth_from_sunlight = 1 - (self.ideal_sunlight - sunlight) / (self.ideal_sunlight)
        if (growth_from_sunlight > 0) and (self.sun_recovery_day > 0): # if plant not burning but need to recover
            self.sun_recovery_day -=1
            growth_from_sunlight = 0
        elif growth_from_sunlight < 0: #if plant burnig
            growth_from_sunlight = 0
            self.sun_recovery_day += 1
        return growth_from_sunlight

if __name__ == "__main__":
    weather_history, current_plants = read_data('weather.json'), []
    current_plants.append(Plant(str(input('Do you want a pea plant(0) or a potato plant(1)\n>>> '))))
    for today in weather_history:
        for plant in current_plants:
            plant.grow(weather_history[today])
            print(plant.sun_recovery_day, plant.water_recovery_day, plant.temp_recovery_day)
            print(plant.my_height)