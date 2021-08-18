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
        send_msg_id = 1
        recv_msg_id = 1
        player_joined_msg = {
            "msg_id" : send_msg_id,
            "player_id" : player_id,
            "msg" : "new_connection",
        }
        self.send(player_joined_msg)
        print(f'player_{checked_player_id} joined!')
        game_engine = ge()
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