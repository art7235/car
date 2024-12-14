import pygame
from os import path
import random

all_sprites = pygame.sprite.Group()
bullets_enemy = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player_group = pygame.sprite.Group()
powerups = pygame.sprite.Group()


def reset():
    global all_sprites, mobs, bullets, powerups
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
