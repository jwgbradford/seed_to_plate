from network import ConnectionManager as CM

class ClientGame():
    def __init__(self) -> None:
        self.score = 0
        self.my_plants = []
        self.inventory = {}

    def run(self):
        cm = CM()

if __name__ == '__main__':
    my_game = ClientGame()
    my_game.run()