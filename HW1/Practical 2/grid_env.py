# grid_env.py
# Random grid world with pygame visualization
# Obstacles, hard terrain, moving obstacles included
# After finishing the search 

import pygame
import copy
import time
import random
import sys
import math
from search import depth_first_search, breadth_first_search, uniform_cost_search, a_star_search

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 15, 15
CELL_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

def generate_grid():
    grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
    for _ in range(40):
        x, y = random.randrange(ROWS), random.randrange(COLS)
        grid[x][y] = None
    for _ in range(30):
        x, y = random.randrange(ROWS), random.randrange(COLS)
        if grid[x][y] == 1:
            grid[x][y] = 5
    return grid

def random_empty_cell(grid):
    while True:
        x, y = random.randrange(ROWS), random.randrange(COLS)
        if grid[x][y] is not None:
            return (x, y)

def heuristic_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic_euclidean(a, b):
    return math.sqrt(abs(a[0] - b[0]) ** 2 + abs(a[1] - b[1]) ** 2)

def get_neighbors_fn(grid, weighted=False):
    def neighbors(pos):
        x, y = pos
        results = []
        for dx, dy in [(0,1),(1,0),(-1,0),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < ROWS and 0 <= ny < COLS:
                if grid[nx][ny] is not None:
                    if weighted:
                        results.append(((nx, ny), grid[nx][ny]))  
                    else:
                        results.append((nx, ny))  
        return results
    return neighbors

def draw_grid(screen, grid, start, goal, current_pos):
    for x in range(ROWS):
        for y in range(COLS):
            rect = pygame.Rect(y*CELL_SIZE, x*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (x, y) == start:
                color = GREEN
            elif (x, y) == goal:
                color = RED
            elif grid[x][y] is None:
                color = BLACK
            elif grid[x][y] == 5:
                color = BROWN
            elif grid[x][y] == 2:
                color= (0,220,0)
            elif grid[x][y] == 3:
                color= (128,0,128)
            else:
                color = WHITE
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GREY, rect, 1)

    # draw current agent position
    if current_pos:
        cx, cy = current_pos
        rect = pygame.Rect(cy*CELL_SIZE, cx*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (0,255,255), rect)

def run(start,goal,grid):
    print("\nChoose algorithm:")
    print("1: DFS")
    print("2: BFS")
    print("3: UCS")
    print("4: A* (Manhattan)")
    print("5: A* (Euclidean)")
    choice = input("Enter choice: ")

    if choice == "1":  # DFS
        algo = lambda s, g: depth_first_search(
            s, g, get_neighbors_fn(grid, weighted=False),grid
        )
    elif choice == "2":  # BFS
        algo = lambda s, g: breadth_first_search(
            s, g, get_neighbors_fn(grid, weighted=False),grid
        )
    elif choice == "3":  # UCS
        algo = lambda s, g: uniform_cost_search(
            s, g, get_neighbors_fn(grid, weighted=True),grid
        )
    elif choice == "4":  # A* Manhattan
        algo = lambda s, g: a_star_search(
            s, g, get_neighbors_fn(grid, weighted=True),
            "manhattan",grid
        )
    elif choice == "5":  # A* Euclidean
        algo = lambda s, g: a_star_search(
            s, g, get_neighbors_fn(grid, weighted=True),
            "euclidean",grid
        )
    else:
        print("Invalid choice")
        pygame.quit()
        sys.exit()

    
    start_time = time.perf_counter()
    path = algo(start, goal)
    end_time = time.perf_counter()

    print(f"Exe Time: {end_time - start_time:.6f} seconds")
    return path

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Search Algorithms with Obstacles")

    while True:  # outer loop for restart
        grid = generate_grid()
        copy_grid = copy.deepcopy(grid)
        start = random_empty_cell(grid)
        goal = random_empty_cell(grid)
    

        path = run(start,goal,grid)
        step = 0
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # quit completely
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:  # restart
                        running = False
                    if event.key == pygame.K_s: # run the algos again on the same grid
                        step = 0
                        grid = copy.deepcopy(copy_grid)
                        screen.fill(WHITE)
                        current_pos = start
                        draw_grid(screen, grid, start, goal, current_pos)
                        path = run(start,goal,grid)


            screen.fill(WHITE)
            current_pos = path[step] if path and step < len(path) else start
            draw_grid(screen, grid, start, goal, current_pos)
            pygame.display.flip()

            if path and step < len(path) - 1:
                step += 1

            clock.tick(3)



if __name__ == "__main__":
    main()
