import random
from random import choice

import pygame
import sys
import os

pygame.init()
size = width, height = 1000, 650
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
worm_size = 50
worm_speed = 15
running = True
game_over = False


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


def move(x, y):
    for i in worm_sprites:
        i.rect = i.rect.move(x, y)


class Player(pygame.sprite.Sprite):
    def __init__(self, coord):
        super().__init__(worm_sprites, all_sprites)
        self.image = pygame.Surface([worm_size, worm_size])
        self.rect = pygame.Rect(coord[0], coord[1], worm_size, worm_size)
        self.image.fill('green')

    def update(self, *args):
        global game_over
        if args:
            self.rect = self.rect.move(args[0], args[1])
        if self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height:
            game_over = True


class Leaf(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(leaves_sprites)
        self.image = pygame.transform.scale(load_image(choice(['red_leaf.png', 'green_leaf.png'])), (64, 48))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(0, width - 64), random.randint(0, height - 48)
        if pygame.sprite.spritecollideany(self, all_sprites):
            self.rect.x, self.rect.y = random.randint(0, width - 64), random.randint(0, height - 48)
        all_sprites.add(leaves_sprites)


CREATELEAF = pygame.USEREVENT + 1
pygame.time.set_timer(CREATELEAF, 10000)

all_sprites = pygame.sprite.Group()
worm_sprites = pygame.sprite.Group()
leaves_sprites = pygame.sprite.Group()


start_screen()


def game():
    Leaf()
    for i in range(5):
        Player((200 - worm_size * i, 200))
    x, y = 0, 0
    while running:
        while game_over:
            screen.fill('black')
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                    terminate()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == CREATELEAF:
                Leaf()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    x, y = 0, -worm_size
                if event.key == pygame.K_DOWN:
                    x, y = 0, worm_size
                if event.key == pygame.K_LEFT:
                    x, y = -worm_size, 0
                if event.key == pygame.K_RIGHT:
                    x, y = worm_size, 0
        screen.fill('dark green')
        move(x, y)
        worm_sprites.update(x, y)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(worm_speed)
    pygame.quit()
    quit()


game()
