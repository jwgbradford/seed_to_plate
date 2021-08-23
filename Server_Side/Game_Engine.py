from test import ask_boolean, pick_from_dict
from Data_Handler import read_data, write_data
from Plant_Handler import Tuber, Fruit
from datetime import datetime
import random, os, threading, sys

class GameEngine():
    def __init__(self, player_id):
        self.input_buffer, self.inventory,  self.my_plants = {}, {}, {}
        self.plant_modifiers = read_data('modifiers.json')
        self.score, self.my_id = 0, player_id
        self.output_buffer = {
            "player_id": None,
            "msg_id" : 1,
            "msg" : "send_id",
            "data" : None
            }

    def run(self):
        self.check_player_id()
        plant_db = read_data('plant_db.json')
        load_game_question = 'Do you want to (l)oad a game or open a (n)ew game?'
        if self.ask_boolean(load_game_question, ['l', 'n']):
            self.load_game_state()
        add_plant_answer = self.ask_boolean('Do you want a new plant (y / n)?)', ['y', 'n'])
        while add_plant_answer:
            self.add_plant(plant_db)
            add_plant_answer = self.ask_boolean('Do you want another new plant (y / n)?)', ['y', 'n'])
        self.set_clock()
        self.main_game_loop()

    def check_player_id(self):
        if self.input_buffer["player_id"] == self.player_id:
            pass
        else:
            sys.exit()

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
        plant_db_simple = {key:{"name": plant_db[key]["name"], "decription": plant_db[key]["description"], "cost":plant_db[key]["cost"]} for key in plant_db}
        plant_keys = self.pick_from_dict('Please pick a plant', plant_db_simple)
        for plant_key in plant_keys:
            plant_type = plant_db[plant_key]["type"]
            plant_data = {'type' : plant_type, 'key' : plant_key}
            self.my_plants[f'plant_{plant_key}'] = eval(f'{plant_type}({plant_data})')

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

    def ask_boolean(self, question, options):
        data_to_send = {"question": question, "options": options}
        self.set_output_buffer(data_to_send, 'ask_boolean')
        if self.input_buffer['msg'] != 'answer to boolean question':
            print('client side error')
            sys.exit()
        if self.input_buffer['data'] == options[0]:
            return True
        return False

    def pick_from_dict_code(self, question, options):
        data_to_send = {"question": question, "options": options}
        self.set_output_buffer(data_to_send, 'pick_from_dict')
        if self.input_buffer['msg'] != 'picked options from dict':
            print('client side error')
            sys.exit()
        for option in self.input_buffer['data']: 
            if option not in list(options.keys()):
                print('client side error')
                sys.exit()
        cost_of_objects = 0
        for option in self.input_buffer['data']:
            cost_of_objects += options[option]['cost']
        return cost_of_objects

    def pick_from_dict(self, question, options):
        #data is list of keys
        cost_of_objects = self.pick_from_dict_code(question, options)
        while cost_of_objects > self.score:
            print('can not afords it')
            self.pick_from_dict_code(question, options)
        return self.input_buffer['data']

    def set_output_buffer(self, data_to_send, msg_to_send): 
        dict_to_send = dict(self.output_buffer)
        dict_to_send['data'] = data_to_send
        dict_to_send['msg'] = msg_to_send
        dict_to_send['msg_id'] += 1
        self.output_buffer = dict_to_send 
        while self.input_buffer['msg_id'] < self.set_output_buffer['msg_id']: 
            pass