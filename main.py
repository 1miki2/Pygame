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
    pass


class Leaf(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(leaves_sprites, all_sprites)
        self.image = pygame.transform.scale(load_image(choice(['red_leaf.png', 'green_leaf.png'])), (50, 50))
        self.rect = self.image.get_rect().move(random.randint(0, width), random.randint(0, height))


start_screen()
CREATELEAF = pygame.USEREVENT + 1
pygame.time.set_timer(CREATELEAF, 10000)
all_sprites = pygame.sprite.Group()
leaves_sprites = pygame.sprite.Group()
running = True
Leaf()
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
    clock.tick(30)
pygame.quit()
