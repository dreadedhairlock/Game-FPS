import pygame as py
from settings import *

# Fungsi yang merender tekstur di game
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
        self.win_image = self.get_texture('resources/texture/win.png', RES)

    # Fungsi yang menggambarkan tekstur
    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_hidup_pemain()

    # Fungsi yang menggambarkan screen jika pemain menang
    def menang(self):
        self.screen.blit(self.win_image, (0, 0))

    # Fungsi yang menggambarkan jika pemain mati
    def game_over(self):
        self.screen.blit(self.gambar_mati, (0, 0))

    # Fungsi untuk menggambarkan hidup pemain di bagian kanan atas
    def draw_hidup_pemain(self):
        health = str(self.game.pemain.hidup)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
            self.screen.blit(self.digits['10'], ((i + 1) *self.digit_size, 0))

    #  Fungsi untuk menggambarkan layar jika pemain tertembak
    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    # Fungsi yang mengambarkan langit
    def draw_background(self):
        self.offset_langit = (self.offset_langit + 4.5 * self.game.pemain.rel) %  WIDTH
        self.screen.blit(self.gambar_langit, (-self.offset_langit, 0))
        self.screen.blit(self.gambar_langit, (-self.offset_langit + WIDTH, 0))
        # untuk lantai
        py.draw.rect(self.screen, WARNA_LANTAI, (0, SETENGAH_HEIGHT, WIDTH, HEIGHT))

    #  Fungsi yang menaruh tekstur pada objek. Memanggil raycasting.py
    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    # Fungsi yang mengambil tekstur dari gambar di path
    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = py.image.load(path).convert_alpha()
        return py.transform.scale(texture, res)

    #  Fungsi yang meload tekstur 
    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/texture/1.png'),
            2: self.get_texture('resources/texture/2.png'),
            3: self.get_texture('resources/texture/3.png'),
            4: self.get_texture('resources/texture/4.png'),
        }