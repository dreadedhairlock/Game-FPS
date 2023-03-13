import pygame as py
from settings import *

class ObjectRender:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.gambar_langit = self.get_texture('resources/texture/sky.png', (WIDTH, SETENGAH_HEIGHT))
        self.offset_langit = 0
        self.blood_screen = self.get_texture('resources/texture/blood_screen.png', RES)
        self.digit_size = 90
        self.gambar_digit = [self.get_texture(f'resources/texture/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.gambar_digit))
        self.gambar_mati = self.get_texture('resources/texture/game_over.png', RES)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_hidup_pemain()

    def game_over(self):
        self.screen.blit(self.gambar_mati, (0, 0))

    def draw_hidup_pemain(self):
        health = str(self.game.pemain.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
            self.screen.blit(self.digits['10'], ((i + 1) *self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.offset_langit = (self.offset_langit + 4.5 * self.game.pemain.rel) %  WIDTH
        self.screen.blit(self.gambar_langit, (-self.offset_langit, 0))
        self.screen.blit(self.gambar_langit, (-self.offset_langit + WIDTH, 0))
        # untuk lantai
        py.draw.rect(self.screen, WARNA_LANTAI, (0, SETENGAH_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = py.image.load(path).convert_alpha()
        return py.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/texture/1.png'),
            2: self.get_texture('resources/texture/2.png'),
            3: self.get_texture('resources/texture/3.png'),
            4: self.get_texture('resources/texture/4.png'),
        }