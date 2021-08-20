from Game_Engine import GameEngine
from threading import Thread
import json, socket

class SeedToPlateServer():
    def __init__(self) -> None:
        self.BUFSIZ = 2048
        self.ADDR = ('', 5555)
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
            player_ip, player_port = player_addr.split(" ")
            Thread(target=self.handle_player, args=(player_conn, player_port)).start()

    # each player has a handler thread
    def handle_player(self, conn, player_id):
        ge = GameEngine(player_id)
        Thread(target=ge.run, args=()).start()
        recv_msg_id = 1, 1
        print(f'player_{player_id} joined!')
        while True:
            self.send(ge.output_buffer, conn)
            try:
                data = self.receive(conn)
            except:
                print(f'player_{player_id} left!')
                break
            if data["player_id"] == player_id:
                print('client not valid')
                break
            if data["msg_id"] > recv_msg_id:
                ge.input_buffer = data
                recv_msg_id = data["msg_id"]
        conn.close()

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