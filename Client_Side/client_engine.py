from network import ConnectionManager as CM

class ClientGame():
    def __init__(self) -> None:
        self.score = 0
        self.my_plants = []
        self.inventory = {}

    def run(self) -> None:
        connection_manager = CM()
        instructions = connection_manager.input_buffer
        reply = connection_manager.output_buffer
        my_id = instructions
        print(f'My ID: {my_id}')
        while True:
            for instruction_id in instructions:
                data = instructions[instruction_id]['data']
                msg = instructions[instruction_id]['msg']
                if msg != 'New_Conection':
                    reply[instruction_id] = eval(f'{msg}({data})')

    def ask_boolean(data):
        question = f"{data['question']}\n >>> "
        options = data["options"]
        choice = input(question).lower()[0]
        while choice not in options:
            choice = input(question).lower()[0]
        if choice == options[0]:
            return True
        return False

    def pick_from_dict(data):
        options = data["options"].keys()
        question = f"{data['question']}\n >>> "
        print(json.dumps(data["options"], indent=4))
        choice = input(question).lower()
        while choice not in options:
            print('not a valid awnser')
            choice = input(question).lower()
        return choice

if __name__ == '__main__':
    my_game = ClientGame()
    my_game.run()