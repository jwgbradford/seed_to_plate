from os import read
from Data_Handler import read_data, write_data
from datetime import datetime, timedelta
from Plant_Handler import Tuber, Fruit
import random, os.path

class Game():
    def __init__(self):
        self.my_plants = []
        self.date = self.set_time()

    def run(self):
        game_type = input('Do you want a (n)ew game or (l)oad a game?\n >>> ').lower()
        if game_type == 'l':
            self.load_game()
        elif game_type == 'n':
            new_plant = input('Do you want to add a plant(y/any_key)\n >>> ').lower()
            while new_plant == 'y':
                self.add_plant()
                new_plant = input('Do you want to add a plant(y/any_key)\n >>> ').lower()
        else:
            self.run()
            return
        self.main_game_loop()

    def load_game(self):
        wanted_file = input('enter file name to load\n >>> ')
        while not os.path.isfile(wanted_file):
            wanted_file = input(' enter valid file name\n >>> ')
        plant_dict = read_data(wanted_file)
        for plant in plant_dict:
            current_plant_dict = plant_dict[plant]
            plant_attrs = read_data('plant.json')[current_plant_dict['type']][str(current_plant_dict['key'])]
            current_plant_dict.update(plant_attrs)
            self.my_plants.append(eval(f"{current_plant_dict['type']}({current_plant_dict}, {current_plant_dict['key']})"))

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
        plant_data = plant_db[plant_type][plant_key]
        # eval turning string to python command
        self.my_plants.append(eval(f'{plant_type}({plant_data}, {plant_key})'))

    def set_time(self):
        clock_type = input('Do you wish for realistic time(0) or virtual time(1)\n >>> ')
        while (clock_type != '0') and (clock_type != '1'):
            clock_type = input('Do you wish for realistic time(0) or vitual time(1)\n>>> ')
        if clock_type == '0':
            str_today = datetime.now().strftime("%Y/%m/%d")
        else:
            str_today = input('enter your desired date (dd/mm/yyyy)\n >>> ')
        return datetime.strptime(str_today, "%Y/%m/%d")

    def main_game_loop(self):
        for _ in range(200):
            weather = self.get_weather()
            print(self.date)
            for  i, plant in enumerate(self.my_plants):
                plant.grow(weather)
                print(f'Plant_{i}: {plant.save_game_state()}')
            self.date += timedelta(days=1)
            my_plants = {}
        for i, plant in enumerate(self.my_plants):
            my_plants[f'Plant_{i}'] = plant.save_game_state()
        write_data(my_plants, 'My_Plants.json')

if __name__ ==  "__main__":
    my_game = Game()
    my_game.run()
    print('The Game has ended')
