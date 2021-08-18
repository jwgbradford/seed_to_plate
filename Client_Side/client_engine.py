from network import ConnectionManager as CM

class ClientGame():
    def __init__(self) -> None:
        self.score = 0
        self.my_plants = []
        self.inventory = {}

    def run(self):
        send_msg_id = 1
        initial_msg = {
            "msg_id" : send_msg_id,
            "msg" : "new_connection",
            "data" : 1234}
        connection_manager = CM(initial_msg)
        my_id = connection_manager.receive()
        connection_manager.send(my_id)
        print(f'My ID: {my_id}')
        while True:
            instructions = connection_manager.input_buffer
            for instruction_id in instructions:
                data = instructions[instruction_id]['data']
                msg = instructions[instruction_id]['msg']
                if data != {}:
                    for key in data:
                        print(data[key])
                if msg != None:
                    connection_manager.output_buffer[instruction_id] = input(msg)

if __name__ == '__main__':
    my_game = ClientGame()
    my_game.run()