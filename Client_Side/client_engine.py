from network import ConnectionManager
from threading import Thread
import json

class ClientGame():
    def __init__(self) -> None:
        self.score = 0
        self.my_plants = []
        self.inventory = {}

    def run(self) -> None:
        player_id = input('Please enter player ID')
        while True:
            if msg_id == 1:
                print('### CONNECTED ###')
                reply_data = data['my_id']
                print(f'Your ID: {reply_data}')
            else:
                reply_data = eval(f'{msg}({data}')
            self.make_dict_to_send(output_dict, msg_id, reply_data, msg)

    def ask_boolean(self, data):
        question = f"{data['question']}\n >>> "
        options = data["options"]
        choice = input(question).lower()[0]
        while choice not in options:
            choice = input(question).lower()[0]
        if choice == options[0]:
            return True
        return False

    def pick_from_dict(self, data):
        options = data["options"].keys()
        question = f"{data['question']}\n >>> "
        print(json.dumps(data["options"], indent=4))
        choice = input(question).lower()
        while choice not in options:
            print('not a valid awnser')
            choice = input(question).lower()
        return data[choice] 

    def make_dict_to_send(self, output_dict, msg_id, reply_data, msg):
        output_dict["player_id"], output_dict["msg"]  = self.my_id, msg
        output_dict["msg_id"], output_dict["data"] = msg_id, reply_data
        if not isinstance(output_dict["data"], dict):
            output_dict["data"] = {"reply": reply_data}

if __name__ == '__main__':
    my_game = ClientGame()
    my_game.run()


    input_dict, output_dict = conn_manager.input_buffer, conn_manager.output_buffer
    main_loop = Thread(target=my_game.run, args=(input_dict, output_dict))
    network_handler = Thread(target=conn_manager.client_network_handler)
    network_handler.start()
    main_loop.join()