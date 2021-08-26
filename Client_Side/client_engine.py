from network import ConnectionManager
import json

class ClientGame():
    def __init__(self) -> None:
        self.score = 0
        self.my_plants = []
        self.inventory = {}

    def run(self) -> None:
        self.connection_manager = ConnectionManager()
        send_msg_id = 0
        while True:
            if self.connection_manager.input_buffer['msg_id'] > send_msg_id:
                function_to_call = self.connection_manager.input_buffer['msg']
                data_to_pass = self.connection_manager.input_buffer['data']
                eval(f'self.{function_to_call}({data_to_pass})')
                send_msg_id += 1
                self.connection_manager.output_buffer["msg_id"] = send_msg_id
                print('output buffer: ',self.connection_manager.output_buffer)

    def send_id(self, data):
        player_id = input('Please enter player ID')
        self.connection_manager.output_buffer["player_id"] = player_id
        self.connection_manager.output_buffer["msg"] = "check_id"

    def ask_boolean(self, data):
        question = f"{data['question']}\n >>> "
        choice = input(question).lower()[0]
        while choice not in data["options"].keys():
            choice = input(question).lower()
        self.connection_manager.output_buffer["msg"] = data["options"][choice]

    def get_string(self, data):
        question = f"{data['question']}\n >>> "
        options = data["options"]
        choice = input(question).lower()[0]
        while choice not in options.keys():
            choice = input(question).lower()[0]
        self.connection_manager.output_buffer["msg"] = options[choice]

    def pick_from_dict(self, data):
        options = data["options"].keys()
        choice = None
        print(options)
        if len(options) > 0:
            question = f"{data['question']}\n >>> "
            print(json.dumps(data["options"], indent=4))
            choice = input(question).lower()
            while choice not in options:
                if choice == '':
                    break
                print('not a valid awnser')
                choice = input(question).lower()
        self.connection_manager.output_buffer["msg"] = data["next_func"]
        self.connection_manager.output_buffer["data"] = {"picked" : choice}
        
if __name__ == '__main__':
    my_game = ClientGame()
    my_game.run()