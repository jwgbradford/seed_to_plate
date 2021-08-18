from Game_Engine import GameEngine as ge
from threading import Thread
import json, socket

class SeedToPlateServer():
    def __init__(self) -> None:
        self.BUFSIZ = 2048
        self.ADDR = ('', 5555) #HOST, PORT
        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.SERVER.bind(self.ADDR)
        self.SERVER.listen(5)
        print("Waiting for a connection, Server Started")        

    def main(self):
        self.clients = {} # empty dictionary for client list
        ACCEPT_THREAD = Thread(target=self.accept_new_players)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        self.SERVER.close()

    def accept_new_players(self):
        while True:
            player_conn, player_addr = self.SERVER.accept()
            Thread(target=self.handle_player, args=(player_conn, player_addr)).start()

    # each player has a handler thread
    def handle_player(self, player_conn, player_id):
        self.send(player_id[0], player_conn)
        checked_player_id = self.receive(player_conn)
        print(f'player_{checked_player_id} joined!')
        game_engine = ge()
        recv_msg_id = 0
        while True:
            try:
                data = self.receive(player_conn)
            except:
                print(f'player_{checked_player_id} left!')
                break
            if data["player_id"] != player_id:
                print('client not valid')
                break
            if data["msg_id"] <= recv_msg_id:
                continue 
            elif data["msg_id"] > recv_msg_id + 1:
                print('missing msgs') # add code to re-send missing msg's
            reply = self.input_message_handler(data, game_engine)
            self.send(reply, player_conn)
        player_conn.close()

    def run_game(self, ge):
        game_set = False
        ge.set_modifiers()
        while not game_set:
            game_type = self.send('Do you want a (n)ew game or (l)oad a game?\n >>> ', conn).lower()
            if len(game_type) > 0:
                game_type = game_type[0]
            if game_type == 'l':
                ge.load_game_state()
                game_set = True
            elif game_type == 'n':
                plant_db = self.read_data('plant_db.json')
                new_plant = 'p'
                while new_plant == 'p':
                    ge.add_plant(plant_db)
                    new_plant = self.send('Do you want to add another (p)lant or play the game (any key)\n >>> ', conn).lower()
                    if len(new_plant) > 0:
                        new_plant = new_plant[0]
                ge.set_clock()
                game_set = True
            else:
                self.send('Invaild entry, plese enter n / l')
        ge.main_game_loop()

    def input_message_handler(self, input_data, game_engine):
        if input_data['msg'] == 'load':
            file_id = input_data["file_name"]
            reply = game_engine.load_game_state(file_id) # need to pass saved file data
        return reply

    def client_network_handler(self):
        while True:
            try:
                self.input_buffer = self.receive()
            except:
                print('Connection lost')
                break            
            self.send(self.output_buffer)

    def send(self, data, conn):
        json_data = json.dumps(data)
        try:
            conn.send(json_data.encode())
        except socket.error as error:
            print(error)

    def receive(self, conn):
        try:
            return json.loads(conn.recv(self.BUFSIZ))
        except socket.error as error:
            print(error)
            return error

if __name__ == "__main__":
    stp = SeedToPlateServer()
    stp.main()