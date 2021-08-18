from Data_Handler import read_data, write_data
from Plant_Handler import Tuber, Fruit
from datetime import datetime
import random, os, threading, sys

class GameEngine():
    def __init__(self):
        self.score = 0
        self.my_plants = {}
        self.inventory = {}

    def run(self):
        game_set = False
        self.set_modifiers()
        while not game_set:
            game_type = input('Do you want a (n)ew game or (l)oad a game?\n >>> ').lower()
            if len(game_type) > 0:
                game_type = game_type[0]
            if game_type == 'l':
                self.load_game_state()
                game_set = True
            elif game_type == 'n':
                plant_db = read_data('plant_db.json')
                new_plant = 'p'
                while new_plant == 'p':
                    self.add_plant(plant_db)
                    new_plant = input('Do you want to add another (p)lant or play the game (any key)\n >>> ').lower()
                    if len(new_plant) > 0:
                        new_plant = new_plant[0]
                self.set_clock()
                game_set = True
            else:
                print('Invaild entry, plese enter n / l')
        self.main_game_loop()

    def set_modifiers(self):
        modifiers = read_data('modifiers.json')
        self.plant_modifiers = modifiers

    def load_game_state(self, game_id):
        # needs to go to client
        game_id = input('enter Game ID to load\n >>> ')
        while not os.path.isfile(f'Game{game_id}.json'):
            game_id = input('enter valid ID name\n >>> ')
        # end code to client
        saved_data = read_data(f'Game{game_id}.json')
        self.load_plant_data(saved_data['my_plants'])
        self.inventory = saved_data['my_inventory']
        self.clock_speed, self.score = saved_data['clock_speed'], saved_data['score'] 
        self.date_last_saved = datetime.strptime(saved_data['date_last_saved'], "%Y/%m/%d")
        return saved_data

    def load_plant_data(self, plant_dict):
        for plant_id in plant_dict: # load the values from the dictionary
            print('loading data...')
            plant_data = plant_dict[plant_id]
            self.my_plants[plant_id] = eval(f"{plant_data['type']}({plant_data})")

    def add_plant(self, plant_db): 
        plant_type = self.choose_plant_type(plant_db)
        plant_key = self.choose_plant(plant_db, plant_type)
        plant_data = {'type' : plant_type, 'key' : plant_key}
        new_id = '1'
        if len(self.my_plants) != 0:
            working_id = int(str(self.my_plants.keys()[-1][6:]))
            new_id = str(working_id + 1)
        self.my_plants[f'plant_{new_id}'] = eval(f'{plant_type}({plant_data})')

    def choose_plant_type(self, plant_db):
        plant_type = str(input(str(plant_db.keys()) + '\n enter type of plant\n>>> '))
        while plant_type not in plant_db.keys():
            plant_type = str(input('pick a valid plant type\n enter type of plant\n>>> '))
        return plant_type

    def choose_plant(self, plant_db, plant_type):
        choices = [plant_db[plant_type][data]['name'] for data in plant_db[plant_type]]
        choice = input('pick plant a plant from\n' + str(choices) + '\n >>> ')
        while choice not in choices:
            choice = input('choose again\n pick plant a plant from\n' + str(choices) + '\n >>> ')
        return str(choices.index(choice))

    def set_clock(self):
        self.clock_speed = self.set_clock_speed(self.set_clock_type())
        self.date_last_saved = datetime.strptime(datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d")

    def set_clock_type(self):
        clock_type = input('Do you wish for realistic time(0) or virtual time(1)\n >>> ')
        while (clock_type != '0') and (clock_type != '1'):
            clock_type = input('Do you wish for realistic time(0) or vitual time(1)\n>>> ')
        return clock_type

    def set_clock_speed(self, clock_type):
        if clock_type == '0':
            return 1440 # 24hours * 60minutes
        speed = 0
        while speed == 0:
            speed = abs(float(input('How many minutes in real time, does 1 day virtual time last?\n >>> ')))
        return speed

    def main_game_loop(self):
        self.catch_up_days()
        self.inventory = dict(self.plant_modifiers)
        playing = True
        while playing:
            self.add_inventory_items()
            threading.Event().wait(self.clock_speed * 60)
            self.grow_plants(game_mode='normal')
            still_playing = input('press enter to continue and any other key to stop')
            if still_playing != '':
                playing = False
        self.save_game_state()

    def catch_up_days(self):
        days_to_run = self.get_missed_days()
        while days_to_run > 0:
            try:
                self.grow_plants(game_mode='catchup')
                days_to_run -= 1
            except KeyboardInterrupt:
                self.save_game_state()
                sys.exit()

    def get_missed_days(self):
        todays_date = datetime.strptime(datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d")
        return ((todays_date.day - self.date_last_saved.day) * 1440) / self.clock_speed

    def grow_plants(self, game_mode):
        weather_today = self.get_weather()
        dead_plants = []
        print(weather_today)
        for key in self.my_plants:
            plant = self.my_plants[key]
            if plant.age < plant.days_to_harvest:
                if game_mode == 'normal':
                    plant.grow(weather_today, self.get_modifiers())
                else:
                    plant.grow(weather_today, {'temp': 0, 'sun': 0, 'water': 0})
                print(f'Plant_{key}: {plant.save_game_state()}')
                self.score += plant.health
            else:
                print('Plant expired')
                dead_plants.append(key)
        for key in dead_plants:
            del self.my_plants[key]

    def get_weather(self):
        weather_dict = {
            'type': random.choice(['Snow', 'Normal']),
            'temp': round(random.uniform(9, 21), 2),
            'sun': round(random.uniform(0,8), 2),
            'rainfall': random.uniform(0, 0.13143)
            }
        return weather_dict

    def delete_invetory_item(self, modifier_type, modifier_uid):
        self.inventory[modifier_type][modifier_uid]['uses'] -= 1
        if self.inventory[modifier_type][modifier_uid]['uses'] == 0:
            del self.inventory[modifier_type][modifier_uid]

    def get_modifiers(self):
        pick_modifiers, choices = 'n', []
        modifier_options = dict(self.inventory)
        chosen_modifiers = {'temp': 0, 'sun': 0, 'water': 0}
        pick_modifiers = input('do you wish to pick a modifer (y/any) ')
        while pick_modifiers == 'y':
            for modifier_type in modifier_options:
                for modifier_key in modifier_options[modifier_type]:
                    modifier = modifier_options[modifier_type][modifier_key]
                    print(modifier['name']+': '+modifier['description']+' ('+modifier_key+')')
                    choices.append([modifier_key, modifier_type])
            choice = input('pick a modifer key to use\n >>>')
            while choice not in [option[0] for option in choices]:
                choice = input('pick a real modifer key to use\n >>>')
            for modifier_type in modifier_options:
                if choice[1] == modifier_type[0]:
                    chosen_modifier_type = modifier_type
            chosen_modifier = modifier_options[chosen_modifier_type][choice]
            chosen_modifiers[chosen_modifier_type] = chosen_modifier['power']
            self.delete_invetory_item(chosen_modifier_type, choice)
            del modifier_options[chosen_modifier_type]
            if len(modifier_options) > 0:
                pick_modifiers = input('do you wish for another modifer (y/any) ')
            else:
                pick_modifiers == 'n'
        return chosen_modifiers

    def add_inventory_items(self):
        add_item = input(' do you wish to buy a modifier (y/any) ')
        if len(add_item) == 0:
            add_item = 'z'
        choices = []
        while add_item[0] == 'y':
            for modifier_type in self.plant_modifiers:
                for modifier_key in self.plant_modifiers[modifier_type]:
                    modifier = self.plant_modifiers[modifier_type][modifier_key]
                    print(modifier['name']+': '+modifier['description']+' ('+modifier_key+')')
                    choices.append([modifier_key, modifier_type])
            choice = input('pick a modifer key to add to your inventory\n >>>')
            while choice not in [option[0] for option in choices]:
                choice = input('pick a real modifer key to add to your inventory\n >>>')
            for modifier_type in self.plant_modifiers:
                if choice[1] == modifier_type[0]:
                    chosen_modifier_type = modifier_type
            if self.plant_modifiers[chosen_modifier_type][choice]['price'] > self.score:
                print('cost_to_much')
                add_item = input(' do you wish to try again (y) / anykey\n >>>').lower()
                if len(add_item) == 0:
                    add_item = 'z'
                continue
            if choice in self.inventory[chosen_modifier_type]:
                self.inventory[chosen_modifier_type][choice]['uses'] += self.plant_modifiers[chosen_modifier_type][choice]['uses']
            else:
                self.inventory[chosen_modifier_type][choice] = self.plant_modifiers[chosen_modifier_type][choice]
            add_item = input(' do you wish to buy something else (y) / any key\n >>>').lower()
            if len(add_item) == 0:
                add_item = 'z'

    def save_game_state(self):
        save_date = datetime.today().strftime("%Y/%m/%d")
        game_id = input('Enter a number to save game state into\n >>> ')
        plants_to_write = {plant_id: self.my_plants[plant_id].save_game_state() for plant_id in self.my_plants}
        dict_to_save = {
            'date_last_saved': save_date,
            'clock_speed': self.clock_speed,
            'score': self.score,
            'my_plants': plants_to_write,
            'my_inventory' : self.inventory
        }
        write_data(dict_to_save, f'Game{game_id}.json') #save dict form above in file from game_id


if __name__ ==  "__main__":
    my_game = GameEngine()
    my_game.run()
    print('The Game has ended')