import random
from random import choice

import pygame
import sys
import os

pygame.init()
size = width, height = 1000, 650
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изобржением "{fullname}" не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen():
    pass


def final_screen():
    pygame.time.set_timer(CREATELEAF, 0)


def game():
    screen.fill('dark green')


class Player(pygame.sprite.Sprite):
    def __init__(self, coord):
        super().__init__(all_sprites)
        self.image = pygame.Surface([10, 10])
        self.rect = pygame.Rect(coord[0], coord[1], 10, 10)
        self.image.fill('green')

    def update(self, *args):
        pass


class Leaf(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(leaves_sprites)
        self.image = pygame.transform.scale(load_image(choice(['red_leaf.png', 'green_leaf.png'])), (64, 48))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(0, width - 64), random.randint(0, height - 48)
        if pygame.sprite.spritecollideany(self, all_sprites):
            self.rect.x, self.rect.y = random.randint(0, width - 64), random.randint(0, height - 48)
        all_sprites.add(leaves_sprites)


start_screen()
CREATELEAF = pygame.USEREVENT + 1
pygame.time.set_timer(CREATELEAF, 10000)
all_sprites = pygame.sprite.Group()
leaves_sprites = pygame.sprite.Group()
running = True
Leaf()
for i in range(5):
    Player((200 - 10 * i, 200))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == CREATELEAF:
            Leaf()
    game()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
pygame.quit()
