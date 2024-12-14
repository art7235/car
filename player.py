import pygame
from os import path
from bullet import Bullet
import sprites

WIDTH = 480
HEIGHT = 600
POWERUP_TIME = 5000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
img_dir = path.join(path.dirname(__file__), 'images')
BLACK = (0, 0, 0)
player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()

snd_dir = path.join(path.dirname(__file__), 'snd')
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image = player_img
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.radius = 30
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.gun = 100
        self.image.set_colorkey(BLACK)
        self.shoot_delay = 450
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.restore_gun = pygame.time.get_ticks()

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        # показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        # тайм-аут для бонусов
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.gun < 80:
            now = pygame.time.get_ticks()
            if now - self.restore_gun > 1000:
                self.gun += 1
                self.restore_gun = now

    def shoot(self):
        if self.gun > 0:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                if self.power == 1:
                    bullet = Bullet(self.rect.centerx, self.rect.top, -5, "laserGreen07.png")
                    sprites.all_sprites.add(bullet)
                    sprites.bullets.add(bullet)
                    shoot_sound.play()
                    self.gun -= 2
                if self.power >= 2:
                    bullet1 = Bullet(self.rect.left, self.rect.centery, -5, "laserGreen07.png")
                    bullet2 = Bullet(self.rect.right, self.rect.centery, -5, "laserGreen07.png")
                    sprites.all_sprites.add(bullet1)
                    sprites.all_sprites.add(bullet2)
                    sprites.bullets.add(bullet1)
                    sprites.bullets.add(bullet2)
                    shoot_sound.play()
                    self.gun -= 4

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
