import socket, json
from threading import Thread

class ConnectionManager:
    def __init__(self, send_msg) -> None:
        ADDR = ("localhost", 5555)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.byte_length = 2048
        self.output_buffer = [send_msg]
        self.input_buffer = []
        CLIENT_NETWORK_THREAD = Thread(target=self.client_network_handler)
        CLIENT_NETWORK_THREAD.start()
        CLIENT_NETWORK_THREAD.join()
        self.client.close()

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
        while True:
            recv_msg_id = 1
            try:
                incoming_msg = self.receive()
            except:
                print('Connection lost')
                break
            if incoming_msg["msg_id"] == recv_msg_id:
                self.input_buffer.append(incoming_msg)
                recv_msg_id += 1
            self.send(self.output_buffer)

