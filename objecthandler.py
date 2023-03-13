from sprite_object import *
from npc import *

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

        # Peta sprite
        add_sprite(ObjekSprite(game))
        add_sprite(AnimatedSprite(game))
        add_sprite(AnimatedSprite(game, pos = (2.5, 4.5)))
        add_sprite(AnimatedSprite(game, pos = (10.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos = (14.5, 6.5)))
        add_sprite(AnimatedSprite(game, pos = (15.5, 6.5)))
        add_sprite(AnimatedSprite(game, pos = (6.5, 9.5)))
        add_sprite(AnimatedSprite(game, pos = (8.5, 9.5)))
        add_sprite(ObjekSprite(game, pos = (1.5, 4.5)))
        add_sprite(ObjekSprite(game, pos = (2.5, 6.5)))

        # Peta NPC
        tambah_npc(NPC(game))
        tambah_npc(NPC(game, pos = (15.5, 6.5)))

    def update(self):
        self.npc_position = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def tambah_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)