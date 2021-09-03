from network import ConnectionManager
import json

class ClientGame():
    def __init__(self) -> None:
        self.my_plants, self.inventory = [], {}

    def run(self) -> None:
        send_msg_id = 0
        self.connection_manager = ConnectionManager()
        while True:
            input_dict = self.connection_manager.input_buffer
            if len(input_dict) > 0:
                if input_dict["msg_id"] > send_msg_id:
                    print(input_dict)
                    msg, reply_data = eval(f'self.{input_dict["msg"]}({input_dict["data"]})')
                    self.make_dict_to_send(input_dict["msg_id"], reply_data, msg)
                    send_msg_id = send_msg_id + 1

    def send_id(self, _):
        self.my_id = int(input('what is your player id? \n >>> '))
        return 'got player_id', self.my_id

    def ask_boolean(self, data):
        question = f"{data['question']}\n >>> "
        options = data["options"]
        choice = input(question).lower()[0]
        while choice not in options:
            choice = input(question).lower()[0]
        return 'answer to boolean question', choice

    def pick_from_dict(self, data):
        options = data["options"].keys()
        question = f"{data['question']}\n >>> "
        print(json.dumps(data["options"], indent=4))
        choice = input(question).lower()
        while choice not in options:
            print('not a valid awnser')
            choice = input(question).lower()
        return 'picked options from dict', choice

    def view_current_plant_state(self, data):
        question = 'Do you wish to see the current state of you plant (y/n)'
        if self.ask_boolean({'question': question, 'options': ["y", "n"]}) == 'y':
            print(data)
        return 'displayed plant state', None

    def make_dict_to_send(self, msg_id, reply_data, msg):
        output_dict = dict(self.connection_manager.output_buffer)
        output_dict["player_id"], output_dict["msg"]  = self.my_id, msg
        output_dict["msg_id"], output_dict["data"] = msg_id, reply_data
        self.connection_manager.output_buffer = output_dict

if __name__ == '__main__':
    my_game = ClientGame()
    my_game.run()