import socket, json
from threading import Thread

class ConnectionManager:
    def __init__(self) -> None:
        ADDR = ("localhost", 5555)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.byte_length = 2048
        self.output_buffer = {
            1 : {
            "msg_id" : send_msg_id,
            "msg" : "new_connection",
            "data" : 1234
            }
        }
        self.input_buffer = {
            0: {}
        }
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
        self.msg_id = 1
        while True:
            try:
                incoming_msg = self.receive()
            except:
                print('Connection lost')
                break
            if incoming_msg["msg_id"] not in self.input_buffer.keys():
                self.input_buffer[incoming_msg["msg_id"]] = incoming_msg
                for key in self.input_buffer.keys():
                    if key == self.msg_id + 1:
                        self.msg_id += 1
            if self.msg_id in self.output_buffer:
                self.send(self.output_buffer[self.msg_id])

