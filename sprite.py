import pygame


class Worm(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating = True
        self.a = pygame.image.load('data/1.png')
        self.b = pygame.image.load('data/2.png')
        self.c = pygame.image.load('data/3.png')
        self.sprites.append(pygame.transform.scale(self.a, (650, 400)))
        self.sprites.append(pygame.transform.scale(self.b, (650, 400)))
        self.sprites.append(pygame.transform.scale(self.c, (650, 400)))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]

    def animate(self):
        self.is_animating = True

    def update(self, speed):
        if self.is_animating == True:
            self.current_sprite += 0.2

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = True

            self.image = self.sprites[int(self.current_sprite)]
