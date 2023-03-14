import pygame as py
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from objectrender import *
from sprite_object import *
from objecthandler import *
from weapon import *
from sound import *
from pathfinding import *

# Merupakan main di mana game berjalan

class Game:
    # Inisialisasi parameter game
    def __init__(self):
        py.init()
        py.mouse.set_visible(False)
        self.screen = py.display.set_mode(RES)
        self.clock = py.time.Clock()
        self.delta_time = 1
        self.trigger_global = False
        self.event_global = py.USEREVENT + 0
        py.time.set_timer(self.event_global, 40)
        self.new_game()

    # Mulai Game Baru
    def new_game(self):
        self.peta = Peta(self)
        self.pemain = Pemain(self)
        self.renderobject = ObjectRender(self)
        self.raycasting = Raycasting(self)
        self.objecthandler = HandlerObjek(self)
        self.senjata = Senjata(self)
        self.suara = Suara(self)
        self.carijalan = CariJalan(self)
        py.mixer.music.play(-1)
        # self.staticsprite = ObjekSprite(self)
        # self.animatedsprite = AnimatedSprite(self)

    #  Memperbarui game setiap kali berjalan
    def update(self):
        self.pemain.update()
        self.raycasting.update()
        self.objecthandler.update()
        self.senjata.update()
        # self.staticsprite.update()
        # self.animatedsprite.update()
        py.display.flip()
        self.delta_time = self.clock.tick(FPS)
        py.display.set_caption(f'{self.clock.get_fps() :.1f}')

    # Membuat gambar serta tekstur game
    def draw(self):
        self.renderobject.draw()
        self.senjata.draw()
        # self.peta.draw()
        # self.pemain.draw()

    # Mengecek apakah game berjalan
    def check_events(self):
        self.trigger_global = False
        for event in py.event.get():
            if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
                py.quit()
                sys.exit()
            elif event.type == self.event_global:
                self.trigger_global = True
            self.pemain.single_fire_event(event)

    # Menjalankan game
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()

