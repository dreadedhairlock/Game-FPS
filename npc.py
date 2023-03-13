from sprite_object import *
from random import random, randint, choice

class NPC(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos = (7.5, 5.5),
                 scale = 0.6, shift = 0.38, animation_time = 110):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.gambar_attack = self.get_images(self.path + '/attack')
        self.gambar_death = self.get_images(self.path + '/death')
        self.gambar_idle = self.get_images(self.path + '/idle')
        self.gambar_pain = self.get_images(self.path + '/pain')
        self.gambar_walk = self.get_images(self.path + '/walk')

        self.jarak_attack = randint(3, 5)
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.trigger_pencarian_pemain = False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.logika_lari()
        # self.draw_ray_cast()

    def check_wall(self, x, y):
        return (x, y) not in self.game.peta.peta_dunia

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def gerak(self):
        next_pos = self.game.carijalan.get_path(self.map_pos, self.game.pemain.map_pos)
        next_x, next_y = next_pos

        # py.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))
        if next_pos not in self.game.objecthandler.npc_position:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def serang(self):
        if self.animation_trigger:
            self.game.suara.npc_serang.play()
            if random() < self.accuracy:
                self.game.pemain.get_damage(self.attack_damage)
    
    def animasi_mati(self):
        if not self.alive:
            if self.game.trigger_global and self.frame_counter < len(self.gambar_death) - 1:
                self.gambar_death.rotate(-1)
                self.image = self.gambar_death[0]
                self.frame_counter += 1

    def animasi_sakit(self):
        self.animate(self.gambar_pain)
        if self.animation_trigger:
            self.pain = False

    def cek_tertembak(self):
        if self.ray_cast_value and self.game.pemain.shot:
            if SETENGAH_WIDTH - self.sprite_half_width < self.screen_x < SETENGAH_WIDTH + self.sprite_half_width:
                self.game.suara.npc_sakit.play()
                self.game.pemain.shot = False
                self.pain = True
                self.health -= self.game.senjata.damage
                self.cek_hidup_npc()

    def cek_hidup_npc(self):
        if self.health < 1:
            self.alive = False
            self.game.suara.npc_mati.play() 

    def logika_lari(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            self.cek_tertembak()
            if self.pain:
                self.animasi_sakit()
            elif self.ray_cast_value:
                self.trigger_pencarian_pemain = True
                
                if self.dist < self.jarak_attack:
                    self.animate(self.gambar_attack)
                    self.serang()
                else:
                    self.animate(self.gambar_walk)
                    self.gerak()

            elif self.trigger_pencarian_pemain:
                self.animate(self.gambar_walk)
                self.gerak()
            else: 
                self.animate(self.gambar_idle)
        else:
            self.animasi_mati()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
    
    def ray_cast_player_npc(self):
        if self.game.pemain.map_pos == self.map_pos:
            return True
        
        jarak_dinding_v, jarak_dinding_h = 0, 0
        jarak_player_v, jarak_player_h = 0, 0


        ox, oy = self.game.pemain.pos
        x_map, y_map = self.game.pemain.map_pos

        ray_angle = self.theta
    
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                jarak_player_h = depth_hor
                break
            if tile_hor in self.game.peta.peta_dunia:
                jarak_dinding_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                jarak_player_v = depth_vert
                break
            if tile_vert in self.game.peta.peta_dunia:
                jarak_dinding_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        jarak_player = max(jarak_player_v, jarak_player_h)
        jarak_dinding = max(jarak_dinding_v, jarak_dinding_h)

        if 0 < jarak_player < jarak_dinding or not jarak_dinding:
            return True
        return False
    
    def draw_ray_cast(self):
        py.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            py.draw.line(self.game.screen, 'orange', (100 * self.game.pemain.x, 100 * self.game.pemain.y),
                         (100 * self.x, 100 * self.y), 2)
            
class SoldierNPC(NPC):
    def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos = (5.5, 1.5),
                 scale = 0.6, shift = 0.38, animation_time = 110):
        super().__init__(game, path, pos, scale, shift, animation_time)
        

class SetanCaco(NPC):
    def __init__(self, game, path='resources/sprites/npc/caco_demon/0.png', pos = (11.5, 15.5),
                 scale = 1.0, shift = 0.04, animation_time = 190):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.jarak_attack = 1.0
        self.speed = 0.05
        self.health = 150
        self.attack_damage = 25
        self.accuracy = 0.30


class SetanCyber(NPC):
    def __init__(self, game, path='resources/sprites/npc/cyber_demon/0.png', pos = (6.5, 7.5),
                 scale = 0.6, shift = 0.38, animation_time = 110):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.jarak_attack = 3
        self.speed = 0.055
        self.health = 200
        self.attack_damage = 15
        self.accuracy = 0.20


            