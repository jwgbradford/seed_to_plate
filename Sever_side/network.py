import socket, json

class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sever, self.port = "192.168.1.234", 5555
        self.addr = (self.sever, self.port)
        self.client.connect(self.addr)
        self.byte_length = 2048

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

class Connection_manager:
    def __init__(self) -> None:
        self.output_buffer = {}
        self.input_buffer = {}

    def client_network_handler(self):
        nw = Network()
        while True:
            try:
                self.input_buffer = nw.receive()
            except:
                print('Connection lost')
                break            
            nw.send(self.output_buffer)

    def run(self):
        while True:
            pass