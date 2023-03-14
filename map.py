import pygame as py

# Bentuk peta dari atas
_ = False
minimap = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [4, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, 1, 1, 1],
    [4, _, _, 1, 1, _, _, 1, 1, _, _, 1, 1, _, 1, 1, 1, 1],
    [4, _, _, 2, 2, _, _, 1, 1, 1, 1, 1, 3, _, 1, _, _, 2],
    [4, _, _, _, _, _, _, _, _, _, _, 1, 3, _, _, _, _, 2],
    [4, 1, 1, 1, 1, 1, _, _, _, _, _, 1, 3, _, _, _, _, 2],
    [1, _, _, 2, 2, _, _, _, _, _, _, 1, 3, _, _, _, _, 2],
    [1, _, _, 3, 2, _, _, _, _, _, _, 1, 1, 1, _, _, _, 2],
    [1, _, _, 3, 3, _, _, _, _, _, _, 1, _, _, _, _, _, 2],
    [1, _, _, _, _, _, _, _, _, 1, 1, 1, _, _, _, _, _, 2],
    [1, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, 2],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3],
]

# Kelas yang mendefinisikan peta
class Peta:
    def __init__(self, game):
        self.game = game
        self.minimap = minimap
        self.peta_dunia = {}
        self.rows = len(self.minimap)
        self.cols = len(self.minimap[0])
        self.get_map()

    # Inisialisasi peta
    def get_map(self):
        for j, row in enumerate(self.minimap):
            for i, value in enumerate(row):
                if value:
                    self.peta_dunia[(i,j)] = value

    # Gambarkan peta
    def draw(self):
        [py.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.peta_dunia]