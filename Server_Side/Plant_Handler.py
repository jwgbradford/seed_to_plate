from random import uniform

class Plant():
    def __init__(self, plant_data):
        self.set_independant_attributes()
        self.set_plant_attributes(plant_data)

    def set_independant_attributes(self):
        self.my_flowers, self.my_fruit, self.pollinated_flowers = 0, 0, 0
        self.my_height, self.stored_water, self.age = 0, 0, 0
        self.sun_recovery_day, self.water_recovery_day, self.temp_recovery_day = 0, 0, 0
        self.my_produce = {}
        self.my_branches, self.expected_yield = 1, 1

    def set_plant_attributes(self, plant_model):
        self.my_key = plant_model['uid']
        for key in plant_model:
            setattr(self, key, plant_model[key])
        if plant_model["rate_of_bifurication"] == 0:
            self.rate_of_bifurication = self.set_bifurication_rate()
        self.daily_growth_rate = self.final_height/self.days_to_harvest

    def add_branches(self):
        for i in range(self.my_branches):
            branching = uniform(0,1)
            if branching > self.rate_of_bifurication:
                self.my_branches += 1

    def set_bifurication_rate(self):
        rate_of_bifurication = 0
        good_enough = False
        cycles = 10
        while not good_enough:
            cumulative_days = 0
            for i in range(cycles):
                day = 0
                branches = 1
                while branches < self.ideal_branches:
                    for i in range(branches):
                        branch_chance = uniform(0, 1)
                        if branch_chance > rate_of_bifurication:
                            branches += 1
                    day += 1
                cumulative_days += day
            average_days = cumulative_days / cycles
            if average_days > self.days_to_flower:
                good_enough = True
            rate_of_bifurication += 0.0001
        return rate_of_bifurication

    def grow(self, weather_today, modifiers):
        self.age += 1
        print(modifiers)
        sunlight_modifier = self.growth_modifier_sunlight(weather_today['sun'], modifiers['sun'])
        hydration_modifier = self.growth_modifier_hydration(weather_today['rainfall'],  modifiers['water'])
        temperature_modifier = self.growth_modifier_temperature(weather_today['temp'], weather_today['type'], modifiers['temp'])
        self.health = self.my_height / (self.daily_growth_rate * self.age)
        if self.age < self.days_to_harvest:
            self.my_height += self.daily_growth_rate * temperature_modifier * hydration_modifier * sunlight_modifier
        self.plant_type_growth()

    def plant_type_growth(self):
        if (self.sun_recovery_day + self.water_recovery_day + self.temp_recovery_day) == 0:
            if (self.age < self.days_to_flower) and (self.my_height > 0):
                self.add_branches()
            elif self.age == self.days_to_flower:
                self.expected_yield = round(self.my_branches / uniform(self.min_fruit_per_branch, self.max_fruit_per_branch))
            elif self.days_to_flower < self.age < self.days_to_fruit:
                if len(self.my_produce) < self.expected_yield:
                    self.add_produce()
                self.grow_produce()
            elif self.days_to_fruit < self.age < self.days_to_harvest:
                self.grow_produce()

    def add_produce(self):
        index = len(self.my_produce)
        for _ in range(self.my_branches):
            if self.health > uniform(0, 0.5) and len(self.my_produce) < self.expected_yield:
                self.my_produce[index] = {
                    "status" : "flower", 
                    "health" : self.health, 
                    "size" : 0
                }
                index += 1

    def grow_produce(self):
        for index in self.my_produce:
            produce = self.my_produce[index]
            if produce["health"] > uniform(0, 0.5):
                if produce["status"] == 'flower':
                    produce["status"] = 'pollinated_flower'
                elif produce["status"] == 'pollinated_flower':
                    produce["status"] = 'fruit'
                else:
                    produce["size"] += produce["health"]
                self.my_produce[index] = produce

    def apply_modifier(self, actual, ideal, modifier_value):
        modifier_effect = (ideal - actual ) * modifier_value
        effective = actual + modifier_effect
        return effective

    def growth_modifier_temperature(self, actual_temp, modifier, modifier_temp):
        temp = self.apply_modifier(actual_temp, self.ideal_temp, modifier_temp)
        if temp > self.ideal_temp:
            growth_from_temp = 1 - (temp - self.ideal_temp) / (self.max_temp - self.ideal_temp)
        elif temp < self.ideal_temp:
            if (modifier == "Snow") and (self.snow_min_temp != "?"):
                growth_from_temp = 1 - (self.ideal_temp - temp) / (self.ideal_temp - self.snow_min_temp)
            else:
                growth_from_temp = 1 - (self.ideal_temp - temp) / (self.ideal_temp - self.min_temp)
        else:
            growth_from_temp = 1
        if (self.temp_recovery_day > 0) and (growth_from_temp > 0):
            self.temp_recovery_day -= 1
            growth_from_temp = 0
        elif growth_from_temp < 0:
            growth_from_temp = 0
            self.temp_recovery_day += 1
        return growth_from_temp

    def growth_modifier_hydration(self, actual_rainfall, modifier_water):
        rainfall = self.apply_modifier(actual_rainfall, self.ideal_water, modifier_water)
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

    def growth_modifier_sunlight(self, actual_sunlight, modifier_light):
        sunlight = self.apply_modifier(actual_sunlight, self.ideal_sunlight, modifier_light)
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
    
    def save_game_state(self):
        return {'key': self.my_key,
                'type': self.__class__.__name__, 
                'name': self.name, 
                'age': self.age, 
                'my_height': self.my_height, 
                'my_branches': self.my_branches, 
                'my_produce': self.my_produce,
                'rate_of_bifurication' : self.rate_of_bifurication}

class Fruit(Plant):
    def __init__(self, plant_data):
        super().__init__(plant_data)

class Tuber(Plant):
    def __init__(self, plant_data):
        super().__init__(plant_data)