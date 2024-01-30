font_style = pygame.font.SysFont(None, 50)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 2 - mesg.get_width() / 2, height / 2 - mesg.get_height() / 2])

def start_screen():
    message('Жми пробел и побежали кушать!', 'blue')
    pygame.display.flip()
    space = False
    while not space:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space = True

def final_screen():
    GameOver()
    pygame.time.set_timer(CREATELEAF, 0)

class GameOver(pygame.sprite.Sprite):
    image = load_image('gameover.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.k = 0
        self.image = pygame.transform.scale(GameOver.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -width, 0

    def update(self, *args):
        if self.rect[0] != 0:
            self.rect = self.rect.move(100, 0)
            clock.tick(100)
