from threading import Thread
from Game_Engine import GameEngine as ge
import json
from socket import socket, AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET

class SeedToPlateServer():
    def __init__(self) -> None:
        ADDR = ('', 5555) #HOST, PORT
        # set up our server socket
        self.BUFSIZ = 2048
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.SERVER.bind(ADDR)
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
        game_engine = ge()
        recv_msg_id = 0
        while True:
            try:
                data = json.loads(player_conn.recv(self.BUFSIZ))
            except:
                print('Connection lost')
                break
            if data["player_id"] != player_id:
                print('client not valid')
                break
            if data["msg_id"] <= recv_msg_id:
                continue 
            elif data["msg_id"] > recv_msg_id + 1:
                print('missing msgs')
                # add code to re-send missing msg's
            reply = self.input_message_handler(data, game_engine)
            json_data = json.dumps(reply)
            player_conn.send(json_data.encode())
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

    def send(self, data):
        json_data = json.dumps(data)
        try:
            self.client.send(json_data.encode())
        except socket.error as error:
            print(error)

    def receive(self):
        try:
            return json.loads(self.client.recv(self.byte_length))
        except socket.error as error:
            return error

if __name__ == "__main__":
    stp = SeedToPlateServer()
    stp.main()