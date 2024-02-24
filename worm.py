import pygame
import sys
import random
from sprite import Worm

WIDTH, HEIGHT = SCREEN_SIZE = (800, 600)
BLOCK_SIZE = 10
WALL_BLOCK = 3
SNAKE_LENGTH = 3
APPLES = 5
INITIAL_GAME_SPEED = 10
SPEED_CHANGE = 1.1
FONT_SIZE = int(WALL_BLOCK * BLOCK_SIZE * 0.75)
SIZE_X, SIZE_Y = WIDTH - WALL_BLOCK * BLOCK_SIZE * 2, HEIGHT - WALL_BLOCK * BLOCK_SIZE * 2

BACKGROUND_COLOR = "dark green"
APPLE_COLOR = "red"
SNAKE_COLOR = "green"
WALL_COLOR = "grey"
TEXT_COLOR = "black"


def main():
    screen, clock = initialize_pygame()
    game_state = initialize_game_state()
    while game_state['program_running']:
        clock.tick(game_state['game_speed'])
        events = get_events()
        update_game_state(events, game_state)
        update_screen(screen, game_state)
    terminate()


def initialize_pygame():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('Worm')
    clock = pygame.time.Clock()
    return screen, clock


def initialize_game_state():
    game_state = {
        "program_running": True,
        "game_running": False,
        "game_paused": False,
        "game_speed": INITIAL_GAME_SPEED,
        "score": 0,
        'max_score': 0,
        "apples": [],
        "snake": []
    }
    return game_state


def get_events():
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            events.append('quit')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                events.append('up')
            elif event.key == pygame.K_DOWN:
                events.append('down')
            elif event.key == pygame.K_RIGHT:
                events.append('right')
            elif event.key == pygame.K_LEFT:
                events.append('left')
            elif event.key == pygame.K_RETURN:
                events.append('enter')
            elif event.key == pygame.K_SPACE:
                events.append('space')
            elif event.key == pygame.K_ESCAPE:
                events.append('escape')
    return events


def update_game_state(events, game_state):
    check_key_presses(events, game_state)
    if game_state['game_running'] and not game_state['game_paused']:
        move_snake(game_state)
        check_collisions(game_state)
        check_apple_consumption(game_state)


def check_key_presses(events, game_state):
    if 'quit' in events:
        game_state["program_running"] = False
    elif not game_state['game_running']:
        if 'escape' in events:
            game_state['program_running'] = False
        elif 'enter' in events:
            initialize_new_game(game_state)
            game_state['game_running'] = True
    elif game_state['game_paused']:
        if 'escape' in events:
            game_state['game_running'] = False
        elif 'space' in events:
            game_state['game_paused'] = False
    else:
        if 'escape' in events or 'space' in events:
            game_state['game_paused'] = True
        if 'up' in events:
            game_state['direction'] = (0, -BLOCK_SIZE)
        if 'down' in events:
            game_state['direction'] = (0, BLOCK_SIZE)
        if 'right' in events:
            game_state['direction'] = (BLOCK_SIZE, 0)
        if 'left' in events:
            game_state['direction'] = (-BLOCK_SIZE, 0)


def move_snake(game_state):
    x = game_state['snake'][0][0] + game_state['direction'][0]
    y = game_state['snake'][0][1] + game_state['direction'][1]
    game_state['snake'].insert(0, (x, y))


def check_collisions(game_state):
    x, y = game_state['snake'][0]
    if x < 0 or y < 0 or x >= SIZE_X - 10 or y >= SIZE_Y - 10 or len(game_state['snake']) > len(
            set(game_state['snake'])):
        game_state['game_running'] = False


def check_apple_consumption(game_state):
    apples_eaten = 0
    for apple in game_state['apples']:
        if apple == game_state['snake'][0]:
            game_state['apples'].remove(apple)
            place_apples(1, game_state)
            game_state['score'] += 1
            update_max_score(game_state)
            apples_eaten += 1
            game_state['game_speed'] = round(game_state['game_speed'] * SPEED_CHANGE)
    if apples_eaten == 0:
        game_state['snake'].pop()


def update_max_score(game_state):
    if game_state['score'] > game_state['max_score']:
        game_state['max_score'] = game_state['score']


def initialize_new_game(game_state):
    place_snake(SNAKE_LENGTH, game_state)
    place_apples(APPLES, game_state)
    game_state['direction'] = (BLOCK_SIZE, 0)
    game_state['game_paused'] = False
    game_state['score'] = 0
    game_state['game_speed'] = INITIAL_GAME_SPEED


def place_snake(length, game_state):
    x, y = round(SIZE_X // 2, -1), round(SIZE_Y // 2, -1)
    game_state['snake'].append((x, y))
    for i in range(1, length):
        game_state['snake'].append((x - i, y))


def place_apples(apples, game_state):
    x = random.randrange(WALL_BLOCK * BLOCK_SIZE, SIZE_X - BLOCK_SIZE, 10)
    y = random.randrange(WALL_BLOCK * BLOCK_SIZE, SIZE_Y - BLOCK_SIZE, 10)
    for i in range(apples):
        while (x, y) in game_state['apples'] or (x, y) in game_state['snake']:
            x = random.randrange(WALL_BLOCK * BLOCK_SIZE, SIZE_X - 1, 10)
            y = random.randrange(WALL_BLOCK * BLOCK_SIZE, SIZE_Y - 1, 10)
        game_state['apples'].append((x, y))


def update_screen(screen, game_state):
    screen.fill(BACKGROUND_COLOR)
    if not game_state['game_running']:
        print_new_game_message(screen)
    elif game_state['game_paused']:
        print_new_paused_message(screen)
    else:
        draw_apples(screen, game_state['apples'])
        draw_snake(screen, game_state['snake'])
    draw_walls(screen)
    print_score(screen, game_state['score'])
    print_max_score(screen, game_state['max_score'])
    pygame.display.flip()


# sprites
moving_sprites = pygame.sprite.Group()
player = Worm(410, 350)
moving_sprites.add(player)


def print_new_game_message(screen):
    font = pygame.font.SysFont('Courier New', FONT_SIZE, bold=True)
    text1 = font.render('Press ENTER to start new game', True, TEXT_COLOR)
    text2 = font.render('Press ESCAPE to quit', True, TEXT_COLOR)
    text_rect1 = text1.get_rect()
    text_rect2 = text2.get_rect()
    text_rect1.center = (WIDTH // 2, HEIGHT // 4.5 - FONT_SIZE // 2)
    text_rect2.center = (WIDTH // 2, HEIGHT // 4.5 + FONT_SIZE // 2)
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)
    moving_sprites.draw(screen)
    moving_sprites.update(0.25)


def print_new_paused_message(screen):
    font = pygame.font.SysFont('Courier New', FONT_SIZE, bold=True)
    text1 = font.render('Press SPACE to continue', True, TEXT_COLOR)
    text2 = font.render('Press ESCAPE to start new game', True, TEXT_COLOR)
    text_rect1 = text1.get_rect()
    text_rect2 = text2.get_rect()
    text_rect1.center = (WIDTH // 2, HEIGHT // 2 - FONT_SIZE // 2)
    text_rect2.center = (WIDTH // 2, HEIGHT // 2 + FONT_SIZE // 2)
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)


def draw_apples(screen, apples):
    for apple in apples:
        x = apple[0] + WALL_BLOCK * BLOCK_SIZE
        y = apple[1] + WALL_BLOCK * BLOCK_SIZE
        pygame.draw.rect(screen, APPLE_COLOR, ((x, y), (BLOCK_SIZE, BLOCK_SIZE)), border_radius=10)


def draw_snake(screen, snake):
    for segment in snake:
        x = segment[0] + WALL_BLOCK * BLOCK_SIZE
        y = segment[1] + WALL_BLOCK * BLOCK_SIZE
        pygame.draw.rect(screen, SNAKE_COLOR, ((x, y), (BLOCK_SIZE, BLOCK_SIZE)), border_radius=10)


def draw_walls(screen):
    wall_size = WALL_BLOCK * BLOCK_SIZE
    pygame.draw.rect(screen, WALL_COLOR, ((0, 0), (WIDTH, wall_size)))
    pygame.draw.rect(screen, WALL_COLOR, ((0, 0), (wall_size, HEIGHT)))
    pygame.draw.rect(screen, WALL_COLOR, ((WIDTH - wall_size, 0), (WIDTH, HEIGHT)))
    pygame.draw.rect(screen, WALL_COLOR, ((0, HEIGHT - wall_size), (WIDTH, HEIGHT)))


def print_score(screen, score):
    font = pygame.font.SysFont('Courier New', FONT_SIZE, bold=True)
    text = font.render('Score: ' + str(score), True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.midleft = (WALL_BLOCK * BLOCK_SIZE, WALL_BLOCK * BLOCK_SIZE // 2)
    screen.blit(text, text_rect)


def print_max_score(screen, score):
    font = pygame.font.SysFont('Courier New', FONT_SIZE, bold=True)
    text = font.render('High score: ' + str(score), True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.midright = (WIDTH - 35, 15)
    screen.blit(text, text_rect)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
