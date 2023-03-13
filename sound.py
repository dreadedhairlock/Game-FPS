import pygame as py

class Suara:
    def __init__(self, game):
        self.game = game
        py.mixer.init()
        self.path = 'resources/sound/'
        self.shotgun = py.mixer.Sound(self.path + 'shotgun.wav')
        self.npc_sakit = py.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_mati = py.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_serang = py.mixer.Sound(self.path + 'npc_attack.wav')
        self.player_sakit = py.mixer.Sound(self.path + 'player_pain.wav')
        self.theme = py.mixer.music.load(self.path + 'theme.wav')