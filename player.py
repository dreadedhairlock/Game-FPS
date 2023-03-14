from settings import *
import pygame as pg
import math

# Kelas yang menyimpan pemain
class Pemain:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.rel = 0
        self.time_prev = pg.time.get_ticks()
        self.hidup= PLAYER_MAX_HEALTH
        self.hidup_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()

    # Game menggunakan regenerating health. Jika pemain tidak ditembak maka hidupnya akan kembali
    # menjadi 100
    def recover_health(self):
        if self.check_health_recovery_delay() and self.hidup< PLAYER_MAX_HEALTH:
            self.hidup+= 1

    # Berapa waktu di mana player tidak ditembak agar hidup kembali regenerate
    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.hidup_recovery_delay:
            self.time_prev = time_now
            return True

    # Mengecek apakah pemain mati
    def cek_mati(self):
        if self.hidup< 1:
            self.game.renderobject.game_over()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()

    # Bagaimana pemain bisa mendapatakan damage
    def get_damage(self, damage):
        self.hidup-= damage
        self.game.renderobject.player_damage()
        self.game.suara.player_sakit.play()
        self.cek_mati()

    # Apa yang terjadi jika senjata ditembakkan
    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.senjata.reloading:
                self.game.suara.shotgun.play()
                self.shot = True
                self.game.senjata.reloading = True

    # Bagaimana pemain bergerak
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

    # Bagaimana pemain melihat dinding
    def check_wall(self, x, y):
        return (x, y) not in self.game.peta.peta_dunia

    # Fungsi agar pemain tidak menembus dinding
    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    # Menggambarkan pemain di minimap. Ini hanya untuk tes
    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math. sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    # Fungsi untuk kontrol mouse
    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_KIRI or mx > MOUSE_BORDER_KANAN:
            pg.mouse.set_pos([SETENGAH_WIDTH, SETENGAH_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    # Fungsi untuk memperbarui kelas
    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()

    # Fungsi untuk menyimpan posisi pemain
    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)