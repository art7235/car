# Игра Shmup - 3 часть
# Cтолкновения и стрельба
import pygame
import random
from os import path
from bullet import Bullet
from mob import Mob
from pow import Pow
from explosion import Explosion
from enemy import Enemy
import sprites
from player import Player



img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

POWERUP_TIME = 5000
WIDTH = 480
HEIGHT = 600
FPS = 40

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), 'images')

font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_blue_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (0, 0, 255))  # Используем синий цвет (RGB: 0, 0, 255)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_bullet_mana_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (0, 0, 255), fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# загрузка всей графики
background = pygame.image.load(path.join(img_dir, 'purple.png')).convert()
background_rect = background.get_rect()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserGreen07.png")).convert()
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)
player_img = pygame.image.load(path.join(img_dir, "playerShip1_red.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)



def newmob():
    m = Mob()
    sprites.all_sprites.add(m)
    sprites.mobs.add(m)


player = Player()
sprites.player_group.add(player)
sprites.all_sprites.add(player)
enemy = 0
for i in range(8):
    newmob()
score = 0
# pygame.mixer.music.play(loops=-1)

last_spawn_time = pygame.time.get_ticks()  # Текущее время в миллисекундах
spawn_interval = 10000  # Интервал спавна врагов в миллисекундах (10 секунд)

# Цикл игры
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        sprites.reset()
        player = Player()
        sprites.all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        # Если игрок умер, игра окончена
        if player.lives == 0 and not death_explosion.alive():
            game_over = True

    current_time = pygame.time.get_ticks()
    # Проверка, прошло ли 10 секунд
    if current_time - last_spawn_time > spawn_interval:
        last_spawn_time = current_time  # Обновляем время последнего спавна
        new_enemy = Enemy()  # Создаем нового врага
        sprites.all_sprites.add(new_enemy)  # Добавляем врага в группу спрайтов
        enemy = 0

    # Обновление
    sprites.all_sprites.update()
    sprites.bullets_enemy.update()
    player.update()

    hits = pygame.sprite.groupcollide(sprites.mobs, sprites.bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        sprites.all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            sprites.all_sprites.add(pow)
            sprites.powerups.add(pow)
        newmob()

    # if enemy == 1:
    #     if new_enemy in all_sprites:
    #         hits = pygame.sprite.spritecollide(player, new_enemy, True, pygame.sprite.collide_circle)
    #         player.shield -= 30
    #         enemy = 0
    #         if player.shield <= 0:
    #             death_explosion = Explosion(player.rect.center, 'player')
    #             all_sprites.add(death_explosion)
    #             player.hide()
    #             player.lives -= 1
    #             player.shield = 100

    hits = pygame.sprite.spritecollide(player, sprites.bullets_enemy, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 10
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            sprites.all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # Проверка столкновений игрока и улучшения
    hits = pygame.sprite.spritecollide(player, sprites.powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

    # Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, sprites.mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        sprites.all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            sprites.all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # Если игрок умер, игра окончена
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    sprites.all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)

    draw_shield_bar(screen, 5, 5, player.shield)
    draw_bullet_mana_bar(screen, 5, 15, player.gun)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # отрисовка всего экрана
    pygame.display.flip()

pygame.quit()
