import pygame
from sys import exit

pygame.init()

# Screen dimensions and pixel size are deeply related, so they are grouped together here.
# The program will crash if these parameters do not afford a complete tiling by tiles of pixel_size X pixel_size
SCREEN_HEIGHT: int = 800  # set these screen variables to a multiple of pixel_size
SCREEN_WIDTH: int = 800
pixel_size: int = 100

# test if pixels tile the screen completely
assert SCREEN_WIDTH % pixel_size == 0 and SCREEN_HEIGHT % pixel_size == 0, \
    'Incompatible SCREEN_WIDTH/HEIGHT and ' \
    'pixel size: \n     Pixel size must divide' \
    ' screen size '

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# preset board templates
vertical_stripe_board = [[i % 2] * (SCREEN_WIDTH // pixel_size)  # 1 is alive, 0 is dead
                         for i in range(SCREEN_HEIGHT // pixel_size)]
empty_board = [[0] * (SCREEN_WIDTH // pixel_size)  # 1 is alive, 0 is dead
               for i in range(SCREEN_HEIGHT // pixel_size)]


# x_y_test_board = empty_board
# x_y_test_board[10][2] = 1


class Board:
    def __init__(self):
        self.n_cols = SCREEN_WIDTH // pixel_size
        self.n_rows = SCREEN_HEIGHT // pixel_size
        self.state = [[0] * self.n_cols for i in range(self.n_rows)]

    def draw(self):
        for x in range(self.n_cols):
            for y in range(self.n_rows):
                if self.state[x][y] == 0:
                    pixel_color = BLACK
                else:
                    pixel_color = WHITE
                pygame.draw.rect(screen, pixel_color, (x * pixel_size, y * pixel_size, pixel_size, pixel_size))

    def eval_surroundings(self, x, y):
        alive = self.state[x][y]
        # corners
        if x == 0 and y == 0:
            neighbors = [self.state[x + a][y + b] for a in [0, 1] for b in [0, 1]]
        elif x == 0 and y == self.n_rows - 1:
            neighbors = [self.state[x + a][y + b] for a in [0, 1] for b in [0, -1]]
        elif x == self.n_cols - 1 and y == 0:
            neighbors = [self.state[x + a][y + b] for a in [0, -1] for b in [0, 1]]
        elif x == self.n_cols - 1 and y == self.n_rows - 1:
            neighbors = [self.state[x + a][y + b] for a in [0, -1] for b in [0, -1]]
        # walls
        elif x == 0:
            neighbors = [self.state[x + a][y + b] for a in [0, 1] for b in [0, 1, -1]]
        elif x == self.n_cols - 1:
            neighbors = [self.state[x + a][y + b] for a in [0, -1] for b in [0, 1, -1]]
        elif y == 0:
            neighbors = [self.state[x + a][y + b] for a in [0, 1, -1] for b in [0, 1]]
        elif y == self.n_rows - 1:
            neighbors = [self.state[x + a][y + b] for a in [0, 1, -1] for b in [0, -1]]
        # interior pixels
        else:
            neighbors = [self.state[x + a][y + b] for a in [0, 1, -1] for b in [0, 1, -1]]
        total = sum(neighbors[1:])

        if not alive:  # returning 1 means cell alive next time-step. Returning 0 means dead.
            if total == 3:
                return 1
            else:
                return 0
        else:
            if total == 2 or total == 3:
                return 1
            else:
                return 0

    def update(self):
        # Copies board and stores changed in temp board
        # otherwise errors occur because, for example, the outcome of evaluating
        # cell N can be changed by the evaluation of cell N - 1
        temp_board = empty_board
        for x in range(self.n_cols):
            for y in range(self.n_rows):
                temp_board[x][y] = self.eval_surroundings(x, y)
        # replace old board state with new results
        self.state = temp_board
        self.draw()

    def flip_pixel(self, x, y):
        # convert into pixel indices
        x = x // pixel_size
        y = y // pixel_size
        if self.state[x][y] == 1:
            self.state[x][y] = 0
        else:
            self.state[x][y] = 1

    def load_board(self, input_board):
        self.state = input_board


board = Board()

tick_speed = 10  # initial clock speed (modifiable during runtime)
run = True
play = False
while run:
    clock.tick(tick_speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # pause and play button
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play = not play
            if event.key == pygame.K_a and tick_speed > 0:
                tick_speed -= 1
                print(f'Tick speed decreased to {tick_speed}')
            if event.key == pygame.K_d:
                tick_speed += 1
                print(f'Tick speed increased to {tick_speed}')
            if event.key == pygame.K_RIGHT:
                board.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            board.flip_pixel(pos[0], pos[1])

    if play:
        board.update()
    else:
        board.draw()
    pygame.display.update()
