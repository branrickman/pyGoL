import pygame
from sys import exit

pygame.init()

# Screen dimensions and pixel size are deeply related, so they are grouped together here.
# The program will crash if these parameters do not afford a complete tiling by tiles of pixel_size X pixel_size
SCREEN_HEIGHT = 800  # set these screen variables to a multiple of pixel_size
SCREEN_WIDTH = 800
pixel_size = 40

# test if pixels tile the screen completely
assert SCREEN_WIDTH % pixel_size == 0 and SCREEN_HEIGHT % pixel_size == 0

screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))
clock = pygame.time.Clock()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# preset boards
stripe_board = [[i % 2] * (SCREEN_WIDTH // pixel_size)  # 1 is alive, 0 is dead
                for i in range(SCREEN_HEIGHT // pixel_size)]
empty_board = [[0] * (SCREEN_WIDTH // pixel_size)  # 1 is alive, 0 is dead
               for i in range(SCREEN_HEIGHT // pixel_size)]
#x_y_test_board = empty_board
#x_y_test_board[10][2] = 1

class Board:
    def __init__(self):
        self.n_cols = SCREEN_WIDTH // pixel_size
        self.n_rows = SCREEN_HEIGHT // pixel_size  # 0 picked arbitrarily, since len is the same for any x in self.state[x]
        self.state = [[0] * self.n_cols for i in range(self.n_rows)]  # 1 is alive, 0 is dead

    def draw(self):
        for x in range(self.n_cols):
            for y in range(self.n_rows):
                if self.state[x][y] == 0:  # (x % 2 == 0 and y % 2 == 0):  # checkerboard test
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

        if not alive:
            if total == 3:
                # print("new life")
                return 1
            else:
                return 0
        else:
            print((x,y))
            print(neighbors)
            print(total, "\n")
            if total == 2 or total == 3:
                # print("survive")
                return 1
            else:
                # print("died")
                return 0


    def update(self):
        temp_board = empty_board
        for x in range(self.n_cols):
            for y in range(self.n_rows):
                print((x, y))
                temp_board[x][y] = self.eval_surroundings(x, y)
        self.state = temp_board
        self.draw()

    def flip_pixel(self, x, y):
        # convert into pixel indices
        # print(f'flipping pixel at {(x, y)}')
        x = x // pixel_size
        y = y // pixel_size
        if self.state[x][y] == 1:
            self.state[x][y] = 0
        else:
            self.state[x][y] = 1
        # print(f'pixel index {(x, y)}')

    def load_board(self, input_board):
        # TODO Figure out a way to create / draw boards, save and load them interactively
        self.state = input_board


board = Board()
#board.load_board(x_y_test_board)
# button = Button()
tick_speed = 10
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
        if pygame.mouse.get_pressed()[0]:
            print("Left mouse click")
            # TODO Pixel flipping seems to be influenced by clock speed (tick_speed). Clicks register, but aren't actually flipping the pixel
            pos = pygame.mouse.get_pos()
            board.flip_pixel(pos[0], pos[1])
    if play:
        board.update()
    else:
        board.draw()
    pygame.display.update()