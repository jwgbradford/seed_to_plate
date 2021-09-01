from Data_Handler import read_data, write_data
from Plant_Handler import Tuber, Fruit
from datetime import datetime
import random, sys

class GameEngine():
    def __init__(self, player_id):
        self.score = 0
        self.my_id = str(player_id)
        self.input_buffer = {
            "player_id": "####",
            "msg_id" : 0,
            "msg" : "waiting",
            "data" : {}
            }
        self.output_buffer = {
            "player_id": "####",
            "msg_id" : 1,
            "msg" : "send_id",
            "data" : {}
            }
        self.my_plants = {}
        self.recv_msg_id = 0
        self.current_plant = 0
        self.chosen_modifiers = {}
        self.permitted_functions = [
            "check_id",
            "load_game",
            "load_saved_data",
            "new_game",
            "load_first_plant",
            "add_plant",
            "real_time",
            "fast_time",
            "set_clock_speed",
            "pick_modifier",
            "grow_plants",
            "record_modifier_choice"
        ]
        self.starting_inventory()

    def starting_inventory(self):
        modifiers = read_data('modifiers.json')
        self.inventory = dict(modifiers)

    def run(self):
        while True:
            if self.input_buffer["msg_id"] > self.recv_msg_id and self.input_buffer["msg"] in self.permitted_functions:
                function_to_call = self.input_buffer["msg"]
                data_to_pass = self.input_buffer["data"]
                self.recv_msg_id = self.input_buffer["msg_id"]
                eval(f'self.{function_to_call}({data_to_pass})')
                self.output_buffer["msg_id"] += 1

    def check_id(self, data):
        if self.input_buffer["player_id"] == self.my_id:
            self.output_buffer["player_id"] = self.my_id
            self.output_buffer["msg"] = "ask_boolean"
            self.output_buffer["data"] = {
                "question" : "Would you like to (l)oad a saved game or start a (n)ew game?",
                "options" : {
                    "l" : "load_game",
                    "n" : "new_game"
                }
            }
        else:
            print('fail')
            # need some method to handle player validation fail

    def load_game(self, data):
        self.output_buffer["msg"] = "pick_from_dict"
        # this should be a proper os call to files on disc
        saved_files = {
                "plant_01" : "my first save file"
            }
        self.output_buffer["data"] = {
            "question" : "Enter Game ID to load",
            "options" : saved_files,
            "next_func" : "load_saved_data"
        }

    def load_saved_data(self, file_name):
        if file_name == None:
            self.check_id(file_name)
        else:
            saved_data = read_data(f'{file_name}.json')
            self.load_plant_data(saved_data['my_plants'])
            self.inventory = saved_data['my_inventory']
            self.clock_speed, self.score = saved_data['clock_speed'], saved_data['score'] 
            self.date_last_saved = datetime.strptime(saved_data['date_last_saved'], "%Y/%m/%d")
            self.output_buffer["msg"] = "load_to_client"
            self.output_buffer["data"] = {
                "plant_01" : "plant data from saved file..."
                }

    def load_plant_data(self, plant_dict):
        plant_db = read_data('plant_db.json')
        for plant_id in plant_dict: # load the values from the dictionary
            print('loading data...')
            uid = plant_dict[plant_id]['uid']
            base_data = plant_db[uid]
            saved_data = plant_dict[plant_id]
            plant_data = {**base_data,  **saved_data}
            self.my_plants[plant_id] = eval(f"{plant_data['type']}({plant_data})")

    def new_game(self, data):
        self.output_buffer["msg"] = "pick_from_dict"
        plant_db = read_data('plant_db.json')
        data_to_send = {plant_key : plant_db[plant_key]['name'] for plant_key in plant_db}
        self.output_buffer["data"] = {
            "question" : "Pick your first plant",
            "options" : data_to_send,
            "next_func" : "load_first_plant"
        }

    def load_plant(self, data): # check plant value against score
        plant_db = read_data('plant_db.json')
        plant_data = plant_db[data['picked']]
        plant_type = plant_data['type']
        new_id = '1'
        if self.score >= plant_data['cost']:
            if len(self.my_plants) != 0:
                working_id = int(str(self.my_plants.keys()[-1][6:]))
                new_id = str(working_id + 1)
            self.my_plants[f'plant_{new_id}'] = eval(f'{plant_type}({plant_data})')
            self.score -= plant_data['cost']
            return True
        else:
            return False

    def load_first_plant(self, data):
        self.score = 999999 # get a free plant to start
        _ = self.load_plant(data)
        self.score = 0
        self.output_buffer["msg"] = "ask_boolean"
        self.output_buffer["data"] = {
            "question" : "Would you like (r)eal time or (f)ast time?",
            "options" : {
                "r" : "real_time",
                "f" : "fast_time"
            }
        }

    def add_plant(self, data):
        if self.load_plant(data):
            question = "Would you like buy another (p)lant or (r)un the game?"
        else:
            question = "You have insufficent funds, would you like buy another (p)lant or (r)un the game?"
        self.output_buffer["msg"] = "ask_boolean"
        self.output_buffer["data"] = {
            "question" : question,
            "options" : {
                "p" : "add_plant",
                "r" : "get_weather"
            }
        }

    def real_time(self, data):
        self.set_clock_speed(1440)

    def fast_time(self, data):
            self.output_buffer["msg"] = "pick_from_dict"
            self.output_buffer["data"] = {
                "question" : "How many minutes in real time, does 1 day virtual time last?",
                "options" : {
                    "0.01" : "1 second",
                    "0.1" : "6 seconds",
                    "1" : "1 minute"
                },
                "next_func" : "set_clock_speed"
            }

    def set_clock_speed(self, data):
        self.clock_speed = data
        self.date_last_saved = datetime.strptime(datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d")
        self.get_weather(data)

    def get_weather(self, data):
        self.current_plant = 0
        weather_dict = {
            'type': random.choice(['Snow', 'Normal']),
            'temp': round(random.uniform(9, 21), 2),
            'sun': round(random.uniform(0,8), 2),
            'rainfall': random.uniform(0, 0.13143)
            }
        self.weather_today = weather_dict
        self.show_weather(weather_dict)

    def show_weather(self, weather_dict):
        question = f'Todays weather is {weather_dict}, do you want to apply a modifier to your plants? (y) / (n)'
        self.output_buffer["msg"] = "ask_boolean"
        self.output_buffer["data"] = {
            "question" : question,
            "options" : {
                "y" : "pick_modifier",
                "n" : "grow_plants"
            }
        }

    def pick_modifier(self, data):
        modifier_options = {
            key : {
                'name' : self.inventory[key]['name'],
                'description' : self.inventory[key]['description']
            } for key in self.inventory
        }
        applied_plant_key = list(self.my_plants)[self.current_plant]
        plant_name = self.my_plants[applied_plant_key].name
        self.output_buffer["msg"] = "multi_from_dict"
        self.output_buffer["data"] = {
            "question" : f'Which modifier would you like to apply to your {plant_name}',
            "options" : modifier_options,
            "next_func" : "record_modifier_choice"
        }

    def record_modifier_choice(self, data):
        modified_plant_key = list(self.my_plants)[self.current_plant]
        print(self.inventory)
        self.chosen_modifiers[modified_plant_key] = {self.inventory[modifier] for modifier in data['picked']}
        for modifier in data['picked']:
            if self.inventory[modifier]['uses'] > 1:
                self.inventory[modifier]['uses'] -= 1
            else:
                del self.inventory[modifier]
        if self.current_plant == len(self.my_plants) - 1:
            self.grow_plants()
        else:
            self.current_plant += 1
            self.show_weather(self.weather_today)

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

    def grow_plants(self, data):
        input('ready to grow plants')
        dead_plants = []
        for key in self.my_plants:
            plant = self.my_plants[key]
            if plant.age < plant.days_to_harvest:
                if self.clock_speed == 1440:
                    plant.grow(self.weather_today, self.chosen_modifiers)
                else:
                    plant.grow(self.weather_today, {'temp': 0, 'sun': 0, 'water': 0})
                print(f'Plant_{key}: {plant.save_game_state()}')
                self.score += plant.health
            else:
                print('Plant expired')
                dead_plants.append(key)
        for key in dead_plants:
            del self.my_plants[key]

    def delete_inventory_item(self, modifier_type, modifier_uid):
        self.inventory[modifier_type][modifier_uid]['uses'] -= 1
        if self.inventory[modifier_type][modifier_uid]['uses'] == 0:
            del self.inventory[modifier_type][modifier_uid]

    def add_inventory_items(self):
        add_item = input(' do you wish to buy a modifier (y/any) ')
        modifiers = read_data('modifiers.json') # need to think about this carefully
        if len(add_item) == 0:
            add_item = 'z'
        choices = []
        while add_item[0] == 'y':
            for modifier_type in modifiers:
                for modifier_key in modifiers[modifier_type]:
                    modifier = modifiers[modifier_type][modifier_key]
                    print(modifier['name']+': '+modifier['description']+' ('+modifier_key+')')
                    choices.append([modifier_key, modifier_type])
            choice = input('pick a modifer key to add to your inventory\n >>>')
            while choice not in [option[0] for option in choices]:
                choice = input('pick a real modifer key to add to your inventory\n >>>')
            for modifier_type in modifiers:
                if choice[1] == modifier_type[0]:
                    chosen_modifier_type = modifier_type
            if modifiers[chosen_modifier_type][choice]['price'] > self.score:
                print('cost_to_much')
                add_item = input(' do you wish to try again (y) / anykey\n >>>').lower()
                if len(add_item) == 0:
                    add_item = 'z'
                continue
            if choice in self.inventory[chosen_modifier_type]:
                self.inventory[chosen_modifier_type][choice]['uses'] += modifiers[chosen_modifier_type][choice]['uses']
            else:
                self.inventory[chosen_modifier_type][choice] = modifiers[chosen_modifier_type][choice]
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

# everything below this is holding for code we may not need
'''
class TempStuff():
    def holding_logic(self): # to be deleted
        # need to think about storing game logic in {} or similar?
        load_game_question = 'Do you want to (l)oad a game or open a (n)ew game?'
        if ask_boolean(load_game_question, ['l', 'n']):
            self.load_game_state()
        plant_db = read_data('plant_db.json')
        self.get_multiple_options(self.add_plant, "ask_boolean('Do you want a new plant (y / n)?', ['y', 'n']", plant_db)
        self.set_clock()
        self.main_game_loop(recv_msg_id)
        #elif self.input_buffer["msg"] not in self.permitted_functions:
        pass # exception handler for non-recognised function calls

    def get_multiple_options(self, func_to_run, get_awnser, pras):
        eval(get_awnser)
        while get_awnser:
            func_to_run(pras)
            eval(get_awnser)
    def old_load_game(self):        
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

    def main_game_loop(self, recv_msg_id):
        self.catch_up_days()
        self.inventory = dict(modifiers)
        playing = True
        while playing:
            self.add_inventory_items()
            threading.Event().wait(self.clock_speed * 60)
            self.grow_plants(game_mode='normal')
            still_playing = input('press enter to continue and any other key to stop')
            if still_playing != '':
                playing = False
        self.save_game_state()

    def get_modifiers(self, data):
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
            self.delete_inventory_item(chosen_modifier_type, choice)
            del modifier_options[chosen_modifier_type]
            if len(modifier_options) > 0:
                pick_modifiers = input('do you wish for another modifer (y/any) ')
            else:
                pick_modifiers == 'n'
        return chosen_modifiers

        if clock_type == '0':
            return 1440 # 24hours * 60minutes
        speed = 0
        while speed == 0:
            speed = abs(float(input('How many minutes in real time, does 1 day virtual time last?\n >>> ')))
        return speed

'''