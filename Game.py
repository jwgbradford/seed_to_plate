from Data_Handler import read_data, random
from datetime import datetime, timedelta
from Plant_Handler import Tuber, Fruit

class Game():
    def __init__(self):
        self.current_plants = []
        self.date_today = self.set_time()
        self.weather = self.get_weather()

    def choose_plant_type(self, plant_db):
        plant_type = str(input(str(plant_db.keys()) + '\n enter type of plant\n>>> '))
        while plant_type not in plant_db.keys():
            plant_type = str(input('pick a valid plant type\n enter type of plant\n>>> '))
        return plant_type

    def choose_plant(self, plant_db, plant_type):
        choices = [plant_db[plant_type][data]['name'] for data in plant_db[plant_type]]
        keys = [plant_db[plant_type][data] for data in plant_db[plant_type]]
        choice = input('pick plant a plant from\n' + str(choices) + '\n >>> ')
        while choice not in choices:
            choice = input('choose again\n pick plant a plant from\n' + str(choices) + '\n >>> ')
        key = keys[choices.index(choice)]
        plant_data = plant_db[plant_type][str(key)]
        return plant_data

    def get_weather(self):
        weather_dict = {
            self.date_today: {
                'type': random.choice(['Snow', 'Normal']),
                'temp': round(random.uniform(9, 21), 2),
                'sun': round(random.uniform(0,8), 2),
                'rainfall': random.uniform(0, 0.13143)
            }
        }

    def add_plant(self): 
        plant_db = read_data('plant.json')
        plant_type = self.choose_plant_type(plant_db)
        plant_data = self.choose_plant(plant_db, plant_type)
        print(plant_data)
        self.current_plants.append(eval(f'{plant_type}({plant_data})'))

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
        for plant in self.current_plants:
            for day in plant.days_to_harvest:
                print(plant.my_height, self.date_today)
                plant.grow(self.weather)
                self.date_today = self.date_today + timedelta(days=1)
                self.weather = self.get_weather()

if __name__ ==  "__main__":
    my_game = Game()
    my_game.add_plant()
    my_game.main_game_loop()
