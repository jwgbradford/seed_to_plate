from Data_Handler import read_data, write_data
from Plant_Handler import Tuber, Fruit
from datetime import datetime
from os import listdir, path
from time import sleep
import sys, random

class GameEngine():
    def __init__(self, player_id):
        self.input_buffer, self.inventory,  self.my_plants = {}, {}, {}
        self.current_folder = path.dirname(path.realpath(__file__))
        self.plant_modifiers = read_data(f'{self.current_folder}/modifiers.json')
        self.save_file_name = 'temorpary_game.json'
        self.score, self.my_id = 1, player_id
        self.output_buffer = {
            "player_id": None,
            "msg_id": 1,
            "msg": "send_id",
            "data": None
            }

    def run(self):
        print(f'player_{self.my_id} joined!')
        print('wating for confirmation')
        while len(self.input_buffer) == 0:
            pass
        print('end of wait')
        self.check_player_id()
        plant_db = read_data(f'{self.current_folder}/plant_db.json')
        load_game_question = 'Do you want to (l)oad a game or open a (n)ew game?'
        if self.ask_boolean(load_game_question, ['l', 'n']):
            self.load_game_state()
        while self.ask_boolean('Do you want a new plant (y / n)?)', ['y', 'n']):
            self.add_plant(plant_db)
        self.set_clock()
        self.main_game_loop()

    def check_player_id(self):
        if self.input_buffer["msg_id"] != 1:
            print('exiting: bad msg_id')
            sys.exit()
        elif self.input_buffer["msg"] != 'got player_id':
            print('exiting: bad msg')
            sys.exit()
        elif self.input_buffer["player_id"] != self.my_id:
            print('exiting: bad player id')
            if self.input_buffer["player_id"] != self.input_buffer["data"]:
                print('exiting: bad data')
            sys.exit()
        print('ID okay')

    def load_game_state(self):
        games_list = [name.spit(".")[0] for name in listdir(f'{self.current_folder}/Games/')]
        games_dict = dict(zip(range(len(games_list)), games_list))
        self.save_file_name = f"{self.pick_from_dict('enter Game ID to load', games_dict)}.json"
        saved_data = read_data(f'{self.current_folder}/Games/{self.save_file_name}') #playes can pick multiple need to fix
        self.inventory, self.score = saved_data['my_inventory'], saved_data['score'] 
        self.clock_speed, plant_data = saved_data['clock_speed'], saved_data['my_plants']
        self.date_last_saved = datetime.strptime(saved_data['date_last_saved'], "%Y/%m/%d")
        self.my_plants[self.save_file_name] = eval(f"{plant_data['type']}({games_dict[self.save_file_name]})")
        return saved_data

    def add_plant(self, plant_db): 
        plant_db_simple = {key:{"name": plant_db[key]["name"], "cost":plant_db[key]["cost"]} for key in plant_db}
        plant_db_simple["null"] = "continue without buying a plant"
        plant_key = self.buy_something('Please pick a plant', plant_db_simple)
        if plant_key != 'null':
            plant_data = {'type': plant_db[plant_key]["type"], 'key': plant_key}
            self.my_plants[f'plant_{plant_key}'] = eval(f'{plant_db[plant_key]["type"]}({plant_data})')

    def set_clock(self):
        self.clock_speed = 1440 #set defult speed to how many minites in a day(24 * 60)
        if self.ask_boolean('Do you wish for realistic time(0) or vitual time(1)', ['1', '0']):
            time_options ={"0": 0.1, "1": 5, "2": 10, "3": 100, "4": 150, "5": 1000, "6": 3000}
            self.clock_speed = time_options[self.pick_from_dict('chose speed', time_options)]
        self.date_last_saved = datetime.strptime(datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d")

    def main_game_loop(self):
        self.catch_up_days()
        self.inventory = dict(self.plant_modifiers)
        while True:
            sleep(self.clock_speed * 60)
            self.grow_plants(game_mode='normal')

    def catch_up_days(self):
        days_to_run = 0
        while self.get_missed_days() > 0:
            self.grow_plants(game_mode='catchup')
            days_to_run -= 1

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
                    plant.grow(weather_today, self.choose_modifiers())
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

    def choose_modifiers(self):
        chosen_modifiers, modifier_options, del_options = [], dict(self.plant_modifiers), {}
        while self.ask_boolean('Do you wish to pick a modifier (y / n)', ['y', 'n']):
            chosen_modifiers.append(self.buy_something('Choose a modifier', modifier_options))
            for modifer_key in modifier_options:
                if modifier_options[modifer_key]["type"] == chosen_modifiers[-1]["type"]:
                    del_options.append(modifer_key)
            for option in del_options:
                del chosen_modifiers[option]
        for modifier_key in chosen_modifiers:
            self.inventory[modifier_key]['uses'] -= 1
            if self.inventory[modifier_key]['uses'] == 0:
                del self.inventory[modifier_key]
        return chosen_modifiers

    def save_game_state(self):
        save_date = datetime.today().strftime("%Y/%m/%d")
        plants_to_write = {plant_id: self.my_plants[plant_id].save_game_state() for plant_id in self.my_plants}
        dict_to_save = {
            'date_last_saved': save_date,
            'clock_speed': self.clock_speed,
            'score': self.score,
            'my_plants': plants_to_write,
            'my_inventory' : self.inventory
        }
        write_data(dict_to_save, f'{self.current_folder}/Games/{self.save_file_name}') #save dict form above in file from game_id

    def ask_boolean(self, question, options):
        data_to_send = {"question": question, "options": options}
        self.set_output_buffer(data_to_send, 'ask_boolean')
        if self.input_buffer['msg'] != 'answer to boolean question':
            print('client side error while awnsering bolean question')
            sys.exit()
        if self.input_buffer['data'] == options[0]:
            return True
        return False

    def buy_something(self, question, options):
        cost_of_object = self.score + 1
        while cost_of_object > self.score:
            _ = self.pick_from_dict(question, options)
            cost_of_object = 0
            if self.input_buffer['data'] != 'null':
                cost_of_object = options[self.input_buffer['data']]['cost']
                question = 'too expensive ty again'
        self.score -= cost_of_object
        return self.input_buffer['data']

    def pick_from_dict(self, question, options):
        self.set_output_buffer({"question": question, "options": options}, 'pick_from_dict')
        if (self.input_buffer['msg'] != 'picked options from dict') or (self.input_buffer['data'] not in options.keys()):
            print('client side error while picking from dict')
            sys.exit()
        return self.input_buffer['data']

    def set_output_buffer(self, data_to_send, msg_to_send): 
        dict_to_send = dict(self.output_buffer)
        dict_to_send['player_id'] = self.my_id
        dict_to_send['data'] = data_to_send
        dict_to_send['msg'] = msg_to_send
        dict_to_send['msg_id'] += 1
        self.output_buffer = dict_to_send 
        while self.input_buffer['msg_id'] < self.output_buffer['msg_id']: 
            pass