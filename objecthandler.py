from sprite_object import *
from npc import *
from random import choices, randrange

# Kelas ini menyimpan semua objek NPC dan sprite
class HandlerObjek:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        tambah_npc = self.tambah_npc
        self.npc_position ={}

        self.enemies = 20  # Banyak NPC
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]
        self.weights = [70, 20, 10]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.spawn_npc()

        # Peta sprite
        add_sprite(ObjekSprite(game))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos = (10.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos = (13.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos = (13.5, 6.5)))
        add_sprite(AnimatedSprite(game, pos = (6.5, 9.5)))
        add_sprite(AnimatedSprite(game, pos = (8.5, 9.5)))
        add_sprite(ObjekSprite(game, pos = (1.5, 4.5)))
        add_sprite(ObjekSprite(game, pos = (15.5, 3.5)))
        add_sprite(ObjekSprite(game, pos = (16.5, 3.5)))
        add_sprite(ObjekSprite(game, pos = (1.5, 4.5)))

        # Peta NPC
        # tambah_npc(NPC(game))

    # Memunculkan NPC berdasarkan acak dengan parameter tertentu
    def spawn_npc(self):
        for i in range(self.enemies):
                npc = choices(self.npc_types, self.weights)[0]
                pos = x, y = randrange(self.game.peta.cols), randrange(self.game.peta.rows)
                while (pos in self.game.peta.peta_dunia) or (pos in self.restricted_area):
                    pos = x, y = randrange(self.game.peta.cols), randrange(self.game.peta.rows)
                self.tambah_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))

    # Fungsi yang menyatakan pemain menang jika semua NPC telah mati
    def check_win(self):
        if not len(self.npc_position):
            self.game.renderobject.menang()
            py.display.flip()
            py.time.delay(1500)
            self.game.new_game()

    # Menaruh NPC (jika hidup) dan NPC berdasarkan yang ditentukan
    def update(self):
        self.npc_position = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        self.check_win()

    # Menambahkan NPC di list
    def tambah_npc(self, npc):
        self.npc_list.append(npc)

    # Menambahkan sprite di list
    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)