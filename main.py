# Игра Shmup - 3 часть
# Cтолкновения и стрельба
import pygame
import random
from os import path
from bullet import Bullet
from mob import Mob
from pow import Pow
from explosion import Explosion

# from enemy import Enemy

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


def spawn():
    last_spawn_time = pygame.time.get_ticks()  # Текущее время в миллисекундах
    spawn_interval = 10000  # Интервал спавна врагов в миллисекундах (10 секунд)

    # running = True
    # while running:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    current_time = pygame.time.get_ticks()
    # Проверка, прошло ли 10 секунд
    if current_time - last_spawn_time > spawn_interval:
        last_spawn_time = current_time  # Обновляем время последнего спавна
        new_enemy = Enemy()  # Создаем нового врага
        all_sprites.add(new_enemy)  # Добавляем врага в группу спрайтов


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
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound.play()
                    self.gun -= 2
                if self.power >= 2:
                    bullet1 = Bullet(self.rect.left, self.rect.centery, -5, "laserGreen07.png")
                    bullet2 = Bullet(self.rect.right, self.rect.centery, -5, "laserGreen07.png")
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    bullets.add(bullet1)
                    bullets.add(bullet2)
                    shoot_sound.play()
                    self.gun -= 4

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()


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
                all_sprites.add(bullet)
                bullets_enemy.add(bullet)
                shoot_sound.play()

    def update(self):
        current_time = pygame.time.get_ticks()  # Текущее время
        self.shoot()
        if current_time - self.creation_time > self.lifetime:  # Проверка на истечение времени жизни
            self.speedy = 7
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT:
                self.kill()  # Убить спрайт (удалить его из всех групп)


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
enemy_player_img = pygame.image.load(path.join(img_dir, "playerShip3_green.png")).convert()


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bullets_enemy = pygame.sprite.Group()
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
all_sprites.add(player)
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
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
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
        all_sprites.add(new_enemy) # Добавляем врага в группу спрайтов
        enemy = 1
    # Обновление
    all_sprites.update()

    player.update()

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
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

    hits = pygame.sprite.spritecollide(player, bullets_enemy, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 10
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # Проверка столкновений игрока и улучшения
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

    # Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # Если игрок умер, игра окончена
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)

    draw_shield_bar(screen, 5, 5, player.shield)
    draw_bullet_mana_bar(screen, 5, 15, player.gun)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    # отрисовка всего экрана
    pygame.display.flip()

pygame.quit()
