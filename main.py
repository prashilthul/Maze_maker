import pygame
import random
import sys

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 40, 40
CELL_SIZE = WIDTH // COLS

WHITE = (240, 240, 240)
BLACK = (30, 30, 30)
VISITED_COLOR = (60, 180, 75)
CURRENT_COLOR = (255, 50, 50)
BG_COLOR = (20, 20, 20)
LINE_COLOR = (200, 200, 200)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()

DIRS = {
    "top": (0, -1),
    "right": (1, 0),
    "bottom": (0, 1),
    "left": (-1, 0),
}
OPPOSITE = {"top": "bottom", "right": "left", "bottom": "top", "left": "right"}


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

    def draw(self, current=False):
        x, y = self.x * CELL_SIZE, self.y * CELL_SIZE

        if self.visited:
            pygame.draw.rect(win, VISITED_COLOR, (x, y, CELL_SIZE, CELL_SIZE))

        if current:
            pygame.draw.rect(win, CURRENT_COLOR, (x, y, CELL_SIZE, CELL_SIZE))

        if self.walls["top"]:
            pygame.draw.line(win, LINE_COLOR, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls["right"]:
            pygame.draw.line(
                win, LINE_COLOR, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2
            )
        if self.walls["bottom"]:
            pygame.draw.line(
                win, LINE_COLOR, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2
            )
        if self.walls["left"]:
            pygame.draw.line(win, LINE_COLOR, (x, y + CELL_SIZE), (x, y), 2)


def get_neighbors(cell, grid):
    neighbors = []
    for direction, (dx, dy) in DIRS.items():
        nx, ny = cell.x + dx, cell.y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS:
            neighbor = grid[ny][nx]
            if not neighbor.visited:
                neighbors.append((direction, neighbor))
    return neighbors


def remove_wall(a, b, direction):
    a.walls[direction] = False
    b.walls[OPPOSITE[direction]] = False


def draw_grid(grid, current=None, message=None):
    win.fill(BG_COLOR)
    for row in grid:
        for cell in row:
            cell.draw(current == cell)
    if message:
        font = pygame.font.SysFont(None, 48)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(1)


def generate_maze(grid, start_cell):
    stack = [start_cell]
    start_cell.visited = True

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = stack[-1]
        neighbors = get_neighbors(current, grid)
        draw_grid(grid, current)

        if neighbors:
            direction, next_cell = random.choice(neighbors)
            remove_wall(current, next_cell, direction)
            next_cell.visited = True
            stack.append(next_cell)
        else:
            stack.pop()


def main():
    grid = [[Cell(x, y) for x in range(COLS)] for y in range(ROWS)]
    generate_maze(grid, grid[0][0])

    draw_grid(grid, message="Maze Complete! Press R to restart or Q to quit")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    grid = [[Cell(x, y) for x in range(COLS)] for y in range(ROWS)]
                    generate_maze(grid, grid[0][0])
                    draw_grid(
                        grid, message="Maze Complete! Press R to restart or Q to quit"
                    )
                    pygame.event.clear()
                    pygame.time.delay(200)
        clock.tick(60)


main()
