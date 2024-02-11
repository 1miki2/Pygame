import pygame
import sys
import random

WIDTH, HEIGHT = SCREEN_SIZE = (800, 600)
BLOCK_SIZE = 10
WALL_BLOCK = 3
INITIAL_GAME_SPEED = 10
BACKGROUND_COLOR = "dark green"
APPLE_COLOR = "red"
SNAKE_COLOR = "green"
WALL_COLOR = "grey"
TEXT_COLOR = "black"
FILE_NAME = "data.txt"
SNAKE_LENGTH = 3
APPLES = 3
RADIUS_APPLE = 5
SIZE_X, SIZE_Y = WIDTH - WALL_BLOCK * BLOCK_SIZE * 2, HEIGHT - WALL_BLOCK * BLOCK_SIZE * 2
apple_sprites = pygame.sprite.Group()
FPS = 30


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
        "game_running": False,
        "game_paused": False,
        "game_speed": INITIAL_GAME_SPEED,
        "score": 0,
        "now": 0,
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
    if x < 0 or y < 0 or x >= SIZE_X or y >= SIZE_Y or len(game_state['snake']) > len(
            set(game_state['snake'])):
        game_state['game_running'] = False
        game_state['apples'] = []


def check_apple_consumption(game_state):
    apples_eaten = 0
    for apple in game_state['apples']:
        if apple == game_state['snake'][0]:
            game_state['apples'].remove(apple)
            place_apples(1, game_state)
            game_state['now'] += 1
            if game_state['now'] > game_state['score']:
                game_state['score'] = game_state['now']
            apples_eaten += 1
            game_state['game_speed'] = round(game_state['game_speed'] * 1.1)
    if apples_eaten == 0:
        game_state['snake'].pop()


def initialize_new_game(game_state):
    game_state['snake'] = []
    place_snake(SNAKE_LENGTH, game_state)
    place_apples(APPLES, game_state)
    game_state['direction'] = (BLOCK_SIZE, 0)
    game_state['game_paused'] = False
    game_state['now'] = 0
    game_state['game_speed'] = INITIAL_GAME_SPEED


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
    print_score(screen, game_state['score'], game_state['now'])
    pygame.display.flip()


def place_apples(apples, game_state):
    x = random.randrange(WALL_BLOCK * BLOCK_SIZE, SIZE_X - BLOCK_SIZE, 10)
    y = random.randrange(WALL_BLOCK * BLOCK_SIZE, SIZE_Y - BLOCK_SIZE, 10)
    for i in range(apples):
        while (x, y) in game_state['apples'] or (x, y) in game_state['snake']:
            x = random.randrange(WALL_BLOCK * BLOCK_SIZE, SIZE_X - 1, 10)
            y = random.randrange(WALL_BLOCK * BLOCK_SIZE, SIZE_Y - 1, 10)
        game_state['apples'].append((x, y))


def place_snake(length, game_state):
    x, y = round(SIZE_X // 2, -1), round(SIZE_Y // 2, -1)
    game_state['snake'].append((x, y))
    for i in range(1, length):
        game_state['snake'].append((x - i, y))


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


def print_score(screen, score, now):
    font = pygame.font.SysFont('Courier New', 24, bold=True)
    text_score = font.render("Score: " + str(score), True, TEXT_COLOR)
    text_rect = text_score.get_rect()
    text_rect.topleft = (WALL_BLOCK * BLOCK_SIZE, 0)
    screen.blit(text_score, text_rect)

    text = font.render("Now:   " + str(now), True, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.topleft = (WALL_BLOCK * BLOCK_SIZE, 0)
    text_rect.y = 30
    screen.blit(text, text_rect)


def print_new_game_message(screen):
    font = pygame.font.SysFont("Courier New", 35, bold=False)
    text_list = ["Нажмите Enter, "
                 "чтобы начать игру",
                 "Или esc, чтобы выйти"]
    string_rendered = font.render(text_list[0], True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord = [SIZE_X // 2 - intro_rect.width // 2, SIZE_Y // 2 - intro_rect.height // 2]
    for line in text_list:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord = [SIZE_X // 2 - intro_rect.width // 2, text_coord[1] + 40]
        intro_rect.y = text_coord[1]
        intro_rect.x = text_coord[0]
        screen.blit(string_rendered, intro_rect)


def print_new_paused_message(screen):
    font = pygame.font.SysFont("Courier New", 35, bold=False)
    text_list = ["ПАУЗА",
                 "чтобы начать игру нажмите Space",
                 "Или esc, чтобы выйти"]
    string_rendered = font.render(text_list[0], True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord = [SIZE_X // 2 - intro_rect.width // 2, 100]
    for line in text_list:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord = [SIZE_X // 2 - intro_rect.width // 2, text_coord[1] + 40]
        intro_rect.y = text_coord[1]
        intro_rect.x = text_coord[0]
        screen.blit(string_rendered, intro_rect)


def terminate():
    pygame.quit()
    sys.exit()


main()
