import pygame
import os
import random


class Boy(pygame.sprite.Sprite):
    def __init__(self, file_name):
        pygame.sprite.Sprite.__init__(self)
        img_file2 = os.path.join(IMG_FILE2, file_name)
        player_img2 = pygame.image.load(img_file2)
        self.image = player_img2.convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        pygame.sprite.collide_rect_ratio(0.7)

        self.rect.x = 0
        self.rect.y = 0

        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        self.speedy = 0
        self.jump_start = 0  # Время начала прыжка

    def update(self):
        now = pygame.time.get_ticks()  # время сейчас
        jump_duration = now - self.jump_start  # длительность прыжка
        if (jump_duration > 200) and self.jump_start != 0:
            self.rect.y += 190
            self.jump_start = 0

        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_RIGHT]:
            self.speedx = 4
        if keystate[pygame.K_LEFT]:
            self.speedx = -8

        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.left < 0:
            self.rect.left = 0


class Villain(Boy):
    def __init__(self, file_name):
        Boy.__init__(self, file_name)

        self.rect.x = 0
        self.rect.y = 0

        self.rect.centerx = WIDTH - 33
        self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        self.speedy = 0

        self.jump_start = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0

        self.speedx = -4
        if self.rect.left < 0:
            self.rect.centerx = WIDTH - 33
            self.rect.bottom = HEIGHT - 10

        self.rect.y += self.speedy
        self.rect.x += self.speedx


class Bullet(Boy):
    def __init__(self, file_name, x, y):
        Boy.__init__(self, file_name)

        self.rect.bottom = y
        self.rect.centerx = x + 30
        self.speedx = 6

    def update(self):
        self.speedx = 6
        self.rect.x += self.speedx


WIDTH = 1800  # Размер игрового окна по шире
HEIGHT = 1000  # Размер игрового окна по высоте
size = WIDTH, HEIGHT
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

GAME_FOLDER2 = os.path.dirname(__file__)
IMG_FILE2 = os.path.join(GAME_FOLDER2, "img2")

# Создаем игру и окно
pygame.init()
pygame.mixer.init()  # инициализируем звук
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
boy = Boy("jerry_idle_anim.gif")
bullet = Bullet("bomb.png", boy.rect.x, boy.rect.y)
# img_file = os.path.join(IMG_FILE2, 'starfield.png')   Создаем путь к файлу file_name, в котором лежит картинка спрайта
# background = pygame.image.load(img_file).convert()

# all_sprites.add(background)
all_sprites.add(bullet)
all_sprites.add(boy)
boys = pygame.sprite.Group()
boys.add(boy)
villain = Villain("blockerMad.png")
all_sprites.add(villain)
villains = pygame.sprite.Group()
villains.add(villain)
all_sprites.add(boy)
all_sprites.add(villains)

# bg = pygame.transform.scale(pygame.image.load('starfield.png'))
# pos_x = 0
# speed = 10


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and boy.jump_start == 0:
                boy.rect.y = boy.rect.y - 190
                boy.jump_start = pygame.time.get_ticks()  # Время начала прыжка  allKeys = pygame.key.get_pressed()

    hits = pygame.sprite.spritecollide(villain, boys, False)
    if hits:
        running = False
    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Обновление
    all_sprites.update()

pygame.quit()
