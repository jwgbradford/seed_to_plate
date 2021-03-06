import socket, json
from threading import Thread

class ConnectionManager:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.output_buffer, self.input_buffer = {}, {}
        self.client.connect(("172.20.4.175", 5555))
        self.byte_length = 2048
        Thread(target=self.client_network_handler, args=()).start()

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
        last_msg_id = 0
        while True:
            try:
                incoming_msg = self.receive()
                #print(incoming_msg)
            except:
                print('Connection lost')
                break
            if incoming_msg["msg_id"] != last_msg_id:
                self.input_buffer = incoming_msg
                last_msg_id = incoming_msg["msg_id"]
            self.send(self.output_buffer)
        self.client.close()