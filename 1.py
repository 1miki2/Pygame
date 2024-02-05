import pygame
import sys
import random

WIDTH, HEIGHT = SCREEN_SIZE = (800, 600)
BLOCK_SIZE = 10
WALL_BLOCK = 3
INITIAL_GAME_SPEED = 10
BACKGROUND_COLOR = "dark green"
SNAKE_LENGTH = 3
APPLES = 3
SIZE_X, SIZE_Y = WIDTH // 2 - WALL_BLOCK * 2, HEIGHT // 2 - WALL_BLOCK * 2


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
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    return screen, clock


def initialize_game_state():
    game_state = {
        "program_running": True,
        "game_running": True,
        "game_paused": False,
        "game_speed": INITIAL_GAME_SPEED,
        "game_score": 0,
        "snake": [],
        "apples": APPLES,
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
    move_snake(game_state)
    check_collisions(game_state)
    check_apple_consumption(game_state)


def check_key_presses(events, game_state):
    if 'quit' in events:
        print(1)
        game_state['program_running'] = False
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
            game_state['direction'] = (0, -1)
        if 'down' in events:
            game_state['direction'] = (0, 1)
        if 'right' in events:
            game_state['direction'] = (1, 0)
        if 'left' in events:
            game_state['direction'] = (-1, 0)


def move_snake(game_state):
    x = game_state['snake'][0][0] + game_state['direction'][0]
    y = game_state['snake'][0][1] + game_state['direction'][1]
    game_state['snake'].insert(0, (x, y))


def check_collisions(game_state):
    x, y = game_state['snake'][0]
    if x < 0 or y < 0 or x >= SIZE_X or y >= SIZE_Y or len(game_state['snake']) > len(set(game_state['snake'])):
        game_state['game_running'] = False


def check_apple_consumption(game_state):
    for apple in game_state['apples']:
        if apple == game_state['snake'][0]:



def initialize_new_game(game_state):
    place_snake(SNAKE_LENGTH, game_state)
    place_apples(APPLES, game_state)
    game_state['direction'] = []
    game_state['game_paused'] = False
    game_state['score'] = 0
    game_state['game_speed'] = INITIAL_GAME_SPEED


def update_screen(screen, game_state):
    screen.fill(BACKGROUND_COLOR)
    pygame.display.flip()


def place_apples(apples, game_state):
    game_state['apples'] = []
    x = random.randint(0, SIZE_X - 1)
    y = random.randint(0, SIZE_Y - 1)
    for i in range(apples):
        while (x, y) in game_state['apples'] or (x, y) in game_state['snake']:
            x = random.randint(0, SIZE_X - 1)
            y = random.randint(0, SIZE_Y - 1)
        game_state['apples'].append(x, y)


def place_snake(length, game_state):
    x, y = SIZE_X // 2, SIZE_Y // 2
    game_state['snake'].append((x, y))
    for i in range(1, length):
        game_state['snake'].append(x - i, y)


def terminate():
    pygame.quit()
    sys.exit()


main()
