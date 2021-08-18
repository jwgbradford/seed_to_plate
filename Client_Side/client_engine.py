from network import ConnectionManager as CM

class ClientGame():
    def __init__(self) -> None:
        self.score = 0
        self.my_plants = []
        self.inventory = {}

    def run(self):
        ConnectionManager = CM()
        my_id = ConnectionManager.receive()
        ConnectionManager.send(my_id)
        print(f'My ID: {my_id}')
        '''while True:
            instructions = ConnectionManager.input_buffer
            for instruction_id in instructions:
                data = instructions[instruction_id]['data']
                msg = instructions[instruction_id]['msg']
                if data != {}:
                    for key in data:
                        print(data[key])
                if msg != None:
                    ConnectionManager.output_buffer[instruction_id] = input(msg)
        '''

if __name__ == '__main__':
    my_game = ClientGame()
    my_game.run()