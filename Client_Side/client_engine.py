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

    def send_id(self, data):
        player_id = input('Please enter player ID')
        self.connection_manager.output_buffer["player_id"] = player_id
        self.connection_manager.output_buffer["msg"] = "check_entered_id"

    def ask_boolean(self, data):
        question = f"{data['question']}\n >>> "
        print(data["options"])
        choice = input(question).lower()
        while choice not in options:
            choice = input(question).lower()
        self.connection_manager.output_buffer["load_save_game"] = choice

    def get_string(self, data):
        question = f"{data['question']}\n >>> "
        options = data["options"]
        choice = input(question).lower()[0]
        while choice not in options.keys():
            choice = input(question).lower()[0]
        self.connection_manager.output_buffer["msg"] = options[choice]

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