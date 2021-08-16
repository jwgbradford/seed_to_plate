from network import ConnectionManager as CM
from threading import Thread

class ClientGame():
    def __init__(self) -> None:
        self.score = 0
        self.my_plants = []
        self.inventory = {}

    def run(self):
        cm = CM()

if __name__ == '__main__':
    my_game = ClientGame()
    run_game = Thread(target=my_game.run())
    run_game.start()