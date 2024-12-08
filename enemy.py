import pygame
from os import path
import random
from bullet import Bullet
import sprites



WIDTH = 480
HEIGHT = 600
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
snd_dir = path.join(path.dirname(__file__), 'snd')
img_dir = path.join(path.dirname(__file__), 'images')
player_img = pygame.image.load(path.join(img_dir, "playerShip3_green.png")).convert()
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
enemy_player_img = pygame.image.load(path.join(img_dir, "playerShip3_green.png")).convert()

shoot_time = 10000
start_time = pygame.time.get_ticks()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((50, 40))
        self.image_orig = enemy_player_img
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(5, 15)
        self.speedy = 0
        self.last_shot = pygame.time.get_ticks()
        self.a = pygame.time.get_ticks()
        self.creation_time = pygame.time.get_ticks()  # Время создания врага
        self.lifetime = 5000  # Время жизни врага в миллисекундах (10 секунд)
        self.rot = 180
        self.image = pygame.transform.rotate(self.image_orig, self.rot)
        self.shoot_delay = random.randint(250, 500)

    def shoot(self):
        if self.speedy == 0:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bullet = Bullet(self.rect.centerx, self.rect.bottom, 10, "laserRed06.png")
                sprites.all_sprites.add(bullet)
                sprites.bullets_enemy.add(bullet)
                shoot_sound.play()

    def update(self):
        current_time = pygame.time.get_ticks()  # Текущее время
        self.shoot()
        if current_time - self.creation_time > self.lifetime:  # Проверка на истечение времени жизни
            self.speedy = 7
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT:
                self.kill()  # Убить спрайт (удалить его из всех групп)
