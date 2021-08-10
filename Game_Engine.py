from Data_Handler import read_data, write_data
from Plant_Handler import Tuber, Fruit
from datetime import datetime
import random, os, threading
class Game():
    def __init__(self):
        self.playing = ''
        self.my_plants = []

    def run(self):
        game_set = False
        while not game_set:
            game_type = input('Do you want a (n)ew game or (l)oad a game?\n >>> ').lower()[0]
            if game_type == 'l':
                self.load_game_state()
                game_set = True
            elif game_type == 'n':
                new_plant = 'p'
                while new_plant == 'p':
                    self.add_plant()
                    new_plant = input('Do you want to add another (p)lant or play the game (any key)\n >>> ').lower()[0]
                self.set_clock()
                game_set = True
            else:
                print('Invaild entry, plese enter n / l')
        self.main_game_loop()

    def load_game_state(self):
        game_id = input('enter Game ID to load\n >>> ')
        while not os.path.isfile(f'Game{game_id}.json'):
            game_id = input('enter valid ID name\n >>> ')
        saved_data = read_data(f'Game{game_id}.json') # we only want to read the file once
        self.load_plant_data(saved_data['my_plants'])
        self.clock_speed = saved_data['clock_speed']
        self.date_last_saved = datetime.strptime(saved_data['date_last_saved'], "%Y/%m/%d")

    def save_game_state(self):
        save_date = datetime.today().strftime("%Y/%m/%d")
        game_id = input('Enter a number to save game state into\n >>> ')
        plants_to_write = {f'plant_{i}': plant.save_game_state() for i, plant in enumerate(self.my_plants)}
        dict_to_save = {'date_last_saved': save_date, 'clock_speed': self.clock_speed, 'my_plants': plants_to_write}
        write_data(dict_to_save, f'Game{game_id}.json') #save dict form above in file from game_id

    def load_plant_data(self, plant_dict):
        for plant_data in plant_dict.values(): # load the values from the dictionary
            print('loading data...')
            # current_plant_dict.update(plant_dict[current_plant_dict['type']][str(current_plant_dict['key'])])
            self.my_plants.append(eval(f"{plant_data['type']}({plant_data})"))
        print(self.my_plants)

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

    def get_weather(self):
        weather_dict = {
            'type': random.choice(['Snow', 'Normal']),
            'temp': round(random.uniform(9, 21), 2),
            'sun': round(random.uniform(0,8), 2),
            'rainfall': random.uniform(0, 0.13143)
            }
        return weather_dict

    def add_plant(self): 
        plant_db = read_data('plant.json')
        plant_type = self.choose_plant_type(plant_db)
        plant_key = self.choose_plant(plant_db, plant_type)
        plant_data = {'type' : plant_type,
            'key' : plant_key}
        #plant_data = plant_db[plant_type][plant_key]
        # eval turning string to python command
        self.my_plants.append(eval(f'{plant_type}({plant_data})'))

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
        return abs(float(input('How many minutes in real time, does 1 day virtual time last?\n >>> ')))

    def get_missed_days(self):
        todays_date = datetime.strptime(datetime.now().strftime("%Y/%m/%d"), "%Y/%m/%d")
        return ((todays_date.day - self.date_last_saved.day) * 1440) / self.clock_speed

    def catch_up_days(self):
        days_to_run = self.get_missed_days()
        while days_to_run > 0:
            self.grow_plants()
            days_to_run -= 1

    def grow_plants(self, modifiers = {}):
        weather_today = self.get_weather()
        for i, plant in enumerate(self.my_plants):
            plant.grow(weather_today, modifiers)
            print(f'Plant_{i}: {plant.save_game_state()}')

    def main_game_loop(self):
        self.catch_up_days()
        while self.playing == '':
            modifiers = {}
            threading.Event().wait(self.clock_speed * 60)
            self.grow_plants(modifiers)
            self.playing = input('press enter to continue and any other key to stop')
        self.save_game_state()

if __name__ ==  "__main__":
    my_game = Game()
    my_game.run()
    print('The Game has ended')