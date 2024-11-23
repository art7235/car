import pygame
from os import path
import random
from bullet import Bullet

WIDTH = 480
HEIGHT = 600
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
snd_dir = path.join(path.dirname(__file__), 'snd')
img_dir = path.join(path.dirname(__file__), 'images')
player_img = pygame.image.load(path.join(img_dir, "playerShip3_green.png")).convert()
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))

shoot_time = 10000
start_time = pygame.time.get_ticks()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((50, 40))
        self.image_orig = player_img
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.last_update = pygame.time.get_ticks()
        self.a = pygame.time.get_ticks()

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.a > 1000:
            bullet = Bullet(self.rect.centerx, self.rect.top, "mob")
            shoot_sound.play()

    def update(self):
        current_time = pygame.time.get_ticks()
        shoot = True
        while shoot:
            if current_time - start_time > shoot_time:
                shoot = False
            else:
                self.shoot()

