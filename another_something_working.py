import socket, json
from threading import Thread

class ConnectionManager:
    def __init__(self) -> None:
        ADDR = ("localhost", 5555)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.byte_length = 2048
        self.output_buffer = {}
        self.input_buffer = {}

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
            print(error)
            return error

    def client_network_handler(self):
        recv_msg_id = 0
        while True:
            try:
                data = self.receive()
                if data["msg_id"] <= recv_msg_id:
                    continue 
                elif data["msg_id"] > recv_msg_id + 1:
                    print('missing msgs') # add code to re-send missing msg
                else:
                    self.input_buffer = data
            except:
                print('Connection lost')
                break            
            self.send(self.output_buffer)

    def run(self):
        CLIENT_NETWORK_THREAD = Thread(target=self.client_network_handler)
        CLIENT_NETWORK_THREAD.start()
        while True:
            pass