"""
Drone Navigation with Local Search Algorithms
Controls: SPACE=pause | R=reset | H/S/G=algorithms | ESC=quit
"""

import pygame
import sys
import random
import math
import copy
from queue import Queue

Q = Queue()
TEMP = 10.0
COOLING_RATE = 0.95

# Grid & Display
GRID_ROWS, GRID_COLS = 10, 12
CELL_SIZE, MARGIN = 70, 15
WIDTH = GRID_COLS * CELL_SIZE + MARGIN * 2
HEIGHT = GRID_ROWS * CELL_SIZE + MARGIN * 2 + 80
FPS, DRONE_SPEED = 30, 10.0
WIND_PROB, OBSTACLE_PROB = 0.15, 0.15

# Colors
WHITE, GRAY, LIGHT_GRAY = (255, 255, 255), (200, 200, 200), (230, 230, 230)
BLACK, LIGHT_BLUE, BLUE = (20, 20, 20), (173, 216, 230), (50, 120, 200)
GREEN, RED, ORANGE, DARK = (80, 200, 120), (220, 60, 60), (184, 66, 33), (40, 40, 40)
YELLOW = (255, 255, 0)

# Helper functions for algorithms
def distance(cell1, cell2):
    """Calculate Manhattan distance between two cells"""
    return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

def get_valid_neighbors(cell, grid : "Grid"):
    """Get all valid neighboring cells (not obstacles, within bounds)"""
    #todo
    valid_n = list()
    if cell[0] + 1 < 10 and not grid.is_obstacle(cell[0]+1,cell[1]) : valid_n.append((cell[0]+1,cell[1]))
    if cell[0] - 1 > 0 and not grid.is_obstacle(cell[0]-1,cell[1]) : valid_n.append((cell[0]-1,cell[1]))
    if cell[1] + 1 < 12 and not grid.is_obstacle(cell[0],cell[1]+1) : valid_n.append((cell[0],cell[1]+1))
    if cell[1] - 1 > 0 and not grid.is_obstacle(cell[0],cell[1] - 1) : valid_n.append((cell[0],cell[1] - 1))

    return valid_n

def check_if_block_is_wind(block,grid : "Grid"):
    checking_neighbor = [block[0],block[1]]
    if grid.has_wind(block[0],block[1]):
        diretion = grid.get_wind_direction(block[0],block[1])
        if diretion == 'right' and checking_neighbor[1] < 12 : checking_neighbor[1] += 1
        elif diretion == 'left' and checking_neighbor[1] > 0 : checking_neighbor[1] -=1
        elif diretion == 'up' and checking_neighbor[0] > 0 : checking_neighbor[0] -= 1
        elif diretion == 'down' and checking_neighbor[0] < 10: checking_neighbor[0] += 1

        if grid.is_obstacle(checking_neighbor[0],checking_neighbor[1]) : return False

    return checking_neighbor

def hill_climbing(current, dest, grid : "Grid"):
    """
    Hill Climbing - Always move to the neighbor that gets closest to destination
    Hint: Use get_valid_neighbors() and distance() functions
    Return: next cell (r, c) to move to
    """
    #todo
    neighbors : list = get_valid_neighbors(current,grid )
    best_cost = distance(current,dest)
    main_neighbor = current

    for neighbor in neighbors:
        checking_neighbor = check_if_block_is_wind(neighbor,grid)
        if checking_neighbor :
            dist = distance(checking_neighbor,dest)
            if dist < best_cost :
                best_cost = dist
                main_neighbor = neighbor

    return main_neighbor

def simulated_annealing(current, dest, grid : "Grid"):
    global TEMP,COOLING_RATE

    """
    Simulated Annealing - Sometimes accept worse moves to escape local optimal
    Hint: Accept bad moves with probability based on temperature
    Return: next cell (r, c) to move to
    """
    
    #todo
    neighbors : list = get_valid_neighbors(current,grid)
    current_cost = distance(current,dest)
    main_node = current

    while len(neighbors) > 0:
        next = random.choice(neighbors)
        checking_neighbor = check_if_block_is_wind(next,grid)
        if checking_neighbor:
            next_cost = distance(checking_neighbor,dest)

            if next_cost < current_cost :
                main_node = next
                break
            else :
                r = random.randint(0,100) / 100
                e = - (next_cost - current_cost) / (TEMP)
                p = math.exp(e)
                if p >= r :
                    main_node = next
                    break
                else :
                    neighbors.remove(next)
                
    TEMP *= COOLING_RATE
    return main_node

def genetic_algorithm(current, dest, grid):
    global Q
    """
    Genetic Algorithm - Generate population of moves, evolve, select best
    Hint: Create population from neighbors, evolve over generations
    Return: next cell (r, c) to move to
    """
    population_size = 8
    generations = 3
    #todo
    if len(list(Q.queue)) == 0:
        path = dict()
        path_dest = []

        for item in range(1,population_size+1):
            parent = set()
            now_place = current
            path[item] = []
            for _ in range(3):
                neighbors : list = get_valid_neighbors(now_place,grid)
                random_way = random.choice(neighbors)
                for _ in range(3):
                    if random_way not in parent:
                        break
                    random_way = random.choice(neighbors)

                if random_way[0] - 1  == now_place[0]:
                    path[item].append('UP')
                elif random_way[0] + 1  == now_place[0]:
                    path[item].append('DOWN')
                elif random_way[1] - 1  == now_place[1]:
                    path[item].append('RIGHT')
                elif random_way[1] + 1  == now_place[1]:
                    path[item].append('LEFT')
                parent.add(now_place)
                now_place = random_way
            d = distance(now_place, dest)
            path_dest.append(1 / (d + 1e-6))

        for _ in range(generations):
            new_path = {}
            for item in range(population_size):
                paths = random.choices(list(path.keys()),weights =path_dest,k=2)
                r = random.randint(0,2)
                n_path : list = path[paths[0]][:r]
                n_path.extend(path[paths[1]][r:])
                attempt = 0
                while not is_valid(current,n_path,grid) and attempt < 10 :
                    paths = random.choices(list(path.keys()),weights =path_dest,k=2)
                    r =random.randint(0,2)
                    n_path : list = path[paths[0]][:r]
                    n_path.extend(path[paths[1]][r:])
                    attempt += 1 
                new_path[item] = n_path

            path = copy.deepcopy(new_path)
            for p in path:
                r1 = random.random()
                if r1 > 0.85 :
                    r = random.randint(0,2)
                    mutating_path = copy.deepcopy(path[p])
                    mutating_path[r] = random.choice(['UP','RIGHT','LEFT','DOWN'])
                    if is_valid(current,mutating_path,grid):
                        path[p] = copy.deepcopy(mutating_path)
            for num, moves in path.items():
                end_cell = get_place(current, moves)
                d = distance(end_cell, dest)
                path_dest[num] = 1 / (d + 1e-6)
            
        choosen = random.choices(list(path.values()), weights=path_dest, k=1)[0]
        for item in choosen:
            Q.put(item)

    print(list(Q.queue))
    cell = get_next_place(current,Q.get())
    return tuple(cell)
        

def is_valid(current, path, grid: "Grid"):
    cell = get_place(current, path)
    if 0 < cell[0] < 10 and 0 < cell[1] < 12 and not grid.is_obstacle(cell[0], cell[1]):
        return True
    return False

def cehck_distance(current,dest,path : list):
    cell = get_place(current,path)
    return distance(cell,dest)
    
def get_place(current, path: list):
    cell = [current[0], current[1]]
    for move in path:
        if move == 'UP' and cell[0] > 0:
            cell[0] -= 1
        elif move == 'DOWN' and cell[0] < 9:
            cell[0] += 1
        elif move == 'RIGHT' and cell[1] < 11:
            cell[1] += 1
        elif move == 'LEFT' and cell[1] > 0:
            cell[1] -= 1
    return cell

def get_next_place(current, move):
    cell = [current[0], current[1]]
    if move == 'UP' and cell[0] > 0:
        cell[0] -= 1
    elif move == 'DOWN' and cell[0] < 9:
        cell[0] += 1
    elif move == 'RIGHT' and cell[1] < 11:
        cell[1] += 1
    elif move == 'LEFT' and cell[1] > 0:
        cell[1] -= 1
        
    return cell
    
    
def cell_center(r, c):
    return (MARGIN + c * CELL_SIZE + CELL_SIZE / 2, MARGIN + r * CELL_SIZE + CELL_SIZE / 2)

# Load/Create Images
def load_or_create_image(path, size, fallback_draw):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        fallback_draw(surf)
        return surf

drone_image = load_or_create_image('drone.png', (CELL_SIZE, CELL_SIZE),
    lambda s: pygame.draw.polygon(s, BLUE, [(CELL_SIZE//2, 0), (0, CELL_SIZE), (CELL_SIZE, CELL_SIZE)]))

obstacle_images = []
for name in ['obstacle1.png', 'obstacle2.png']:
    try:
        obstacle_images.append(pygame.transform.scale(pygame.image.load(name), (CELL_SIZE, CELL_SIZE)))
    except: pass
if not obstacle_images:
    obstacle_images = [load_or_create_image('', (CELL_SIZE, CELL_SIZE),
        lambda s: pygame.draw.rect(s, DARK, (0, 0, CELL_SIZE, CELL_SIZE)))]

# Wind indicator
wind_img = load_or_create_image('wind.png', (CELL_SIZE, CELL_SIZE), lambda s: None)
if wind_img.get_at((0,0)).a == 0:  # Failed to load
    wind_img = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    c = CELL_SIZE // 2
    pygame.draw.polygon(wind_img, ORANGE, [(CELL_SIZE-10, c), (10, c-15), (10, c+15)])
    pygame.draw.polygon(wind_img, ORANGE, [(CELL_SIZE-10, c), (CELL_SIZE-25, c-12), (CELL_SIZE-25, c+12)])

wind_rotations = {'up': wind_img, 'down': pygame.transform.rotate(wind_img, 180),
                  'left': pygame.transform.rotate(wind_img, 90), 'right': pygame.transform.rotate(wind_img, -90)}

class Grid:
    """Represents the navigation grid with obstacles and wind"""
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.wind = [[(0, 0) for _ in range(cols)] for _ in range(rows)]
        self.wind_cells = set()
        self.obstacles = {}  # {(r, c): image_index}

    def randomize_wind(self, wind_probability=0.3):
        self.wind_cells.clear()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for r in range(self.rows):
            for c in range(self.cols):
                if random.random() < wind_probability:
                    direction = random.choice(directions)
                    self.wind[r][c] = direction
                    self.wind_cells.add((r, c))
                else:
                    self.wind[r][c] = (0, 0)

    def randomize_obstacles(self, start, dest, prob=0.15):
        self.obstacles = {(r, c): random.randint(0, len(obstacle_images)-1)
                         for r in range(self.rows) for c in range(self.cols)
                         if (r, c) not in [start, dest] and random.random() < prob}

    def is_obstacle(self, r, c): return (r, c) in self.obstacles
    def get_obstacle_image(self, r, c): return obstacle_images[self.obstacles[r, c]] if (r, c) in self.obstacles else None
    def has_wind(self, r, c): return (r, c) in self.wind_cells
    
    def get_wind_direction(self, r, c):
        wx, wy = self.wind[r][c]
        if abs(wx) > abs(wy): return 'right' if wx > 0 else 'left' if wx < 0 else None
        return 'down' if wy > 0 else 'up' if wy < 0 else None

class Drone:
    """Drone that navigates the grid using different algorithms"""
    def __init__(self, start, dest, grid, algorithm='random'):
        self.start, self.destination, self.grid, self.algorithm = start, dest, grid, algorithm
        self.current_cell = self.target_cell = start
        self.path = [start]  # Track all visited cells
        self.reached_destination = False
        self.move_timer = self.animation_progress = 0.0
        self.recent_positions = []  # For loop detection
    
    def get_next_move(self):
        """Call the appropriate algorithm to get next move"""
        algo_map = {'hill_climbing': hill_climbing, 'simulated_annealing': simulated_annealing,
                   'genetic_algorithm': genetic_algorithm}
        if self.algorithm in algo_map:
            return algo_map[self.algorithm](self.current_cell, self.destination, self.grid)
        # Fallback to random movement
        neighbors = get_valid_neighbors(self.current_cell, self.grid)
        return random.choice(neighbors) if neighbors else self.current_cell
    
    def is_in_loop(self, pos):
        """Check if drone is stuck in a loop"""
        #todo
        length = len(self.recent_positions)
        if pos in self.recent_positions[length - 5 :] :
            return True
        return False
    
    def update_recent_positions(self, pos):
        """Track recent positions for loop detection"""
        #todo
        self.recent_positions.append(pos)

    
    def get_wind_pushed_cell(self):
        r, c = self.current_cell
        wx, wy = self.grid.wind[r][c]
        if abs(wx) > abs(wy):
            return (r, max(0, min(self.grid.cols-1, c + (1 if wx > 0 else -1))))
        return (max(0, min(self.grid.rows-1, r + (1 if wy > 0 else -1))), c)
            
    def update(self, dt):
        """Update drone position and handle movement logic"""
        if self.reached_destination: return
        
        # Handle smooth animation between cells
        if self.animation_progress < 1.0:
            self.animation_progress += dt * DRONE_SPEED
            if self.animation_progress >= 1.0:
                self.animation_progress = 1.0
                self.current_cell = self.target_cell
                self.path.append(self.current_cell)
                self.update_recent_positions(self.current_cell)
                
                # Check if reached destination
                if self.current_cell == self.destination:
                    self.reached_destination = True
                    return
                
                # Apply wind push if current cell has wind
                if self.grid.has_wind(*self.current_cell):
                    pushed = self.get_wind_pushed_cell()
                    if pushed != self.current_cell and not self.grid.is_obstacle(*pushed):
                        self.target_cell = pushed
                        self.animation_progress = 0.0
                        return
        else:
            # Ready for next algorithm move
            self.move_timer += dt
            if self.move_timer >= 1.0 / DRONE_SPEED:
                self.move_timer = 0
                next_cell = self.get_next_move()
                
                # Escape loops with random movement
                if self.is_in_loop(next_cell) or next_cell == self.current_cell:
                    neighbors = get_valid_neighbors(self.current_cell, self.grid)
                    next_cell = random.choice(neighbors) if neighbors else self.current_cell
                
                if next_cell in get_valid_neighbors(self.current_cell, self.grid):
                    self.target_cell = next_cell
                    self.animation_progress = 0.0
    
    def get_position(self):
        if self.animation_progress >= 1.0: return cell_center(*self.current_cell)
        curr_pos, target_pos = cell_center(*self.current_cell), cell_center(*self.target_cell)
        t = self.animation_progress
        return (curr_pos[0] + (target_pos[0] - curr_pos[0]) * t,
                curr_pos[1] + (target_pos[1] - curr_pos[1]) * t)
    
    def reset(self, start, dest, algorithm=None):
        self.start, self.destination = start, dest
        self.current_cell = self.target_cell = start
        self.path = [start]
        self.reached_destination = False
        self.move_timer = self.animation_progress = 0.0
        self.recent_positions = []
        if algorithm: self.algorithm = algorithm

def draw_grid(screen, grid, start, dest):
    screen.fill(LIGHT_GRAY)
    for r in range(grid.rows):
        for c in range(grid.cols):
            x, y = MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            
            if grid.is_obstacle(r, c):
                screen.blit(grid.get_obstacle_image(r, c), (x, y))
            elif grid.has_wind(r, c):
                pygame.draw.rect(screen, LIGHT_BLUE, rect)
                wind_dir = grid.get_wind_direction(r, c)
                if wind_dir:
                    screen.blit(wind_rotations[wind_dir], wind_rotations[wind_dir].get_rect(center=cell_center(r, c)))
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)
    
    pygame.draw.rect(screen, GREEN, pygame.Rect(MARGIN + start[1]*CELL_SIZE, MARGIN + start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(MARGIN + dest[1]*CELL_SIZE, MARGIN + dest[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_info(screen, font, status, moves, algorithm):
    pygame.draw.rect(screen, DARK, pygame.Rect(0, HEIGHT-80, WIDTH, 80))
    text = font.render(f"Moves: {moves} | Algorithm: {algorithm} | {status}", True, WHITE)
    screen.blit(text, (MARGIN, HEIGHT-60))

def draw_restart_button(screen, font):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(204)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    button = pygame.Rect((WIDTH-200)//2, (HEIGHT-140)//2, 200, 60)
    pygame.draw.rect(screen, GREEN, button)
    pygame.draw.rect(screen, WHITE, button, 3)
    screen.blit(font.render("RESTART", True, WHITE), font.render("RESTART", True, WHITE).get_rect(center=button.center))
    return button

def get_random_free_cell(grid : Grid , exclude : set):
    """Get a random cell that's not an obstacle or in exclude list"""
    #todo
    r = random.randint(1,9)
    c = random.randint(1,11)

    while grid.is_obstacle(r,c) or grid.has_wind(r,c) or (r,c) in exclude:
        r = random.randint(1,9)
        c = random.randint(1,11)

    return (r,c)


def start_new_game(grid, drone, algorithm):
    min_distance = max(7, (grid.rows + grid.cols) // 4)

    while True:
        start = get_random_free_cell(grid, set())
        dest = get_random_free_cell(grid, {start})
        if distance(start, dest) >= min_distance:
            break

    grid.randomize_obstacles(start, dest, OBSTACLE_PROB)
    grid.randomize_wind(WIND_PROB)
    drone.reset(start, dest, algorithm)
    return f"Navigating with {algorithm}... (min dist = {min_distance})"


def main():
    global TEMP
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Drone Navigation - Local Search")
    clock, font = pygame.time.Clock(), pygame.font.SysFont("Arial", 24, bold=True)

    grid = Grid(GRID_ROWS, GRID_COLS)
    start = get_random_free_cell(grid, set())
    dest = get_random_free_cell(grid, {start})
    grid.randomize_obstacles(start, dest, OBSTACLE_PROB)
    grid.randomize_wind(WIND_PROB)
    
    drone = Drone(start, dest, grid, 'random')
    anim_play, status, flash_shown = True, "Navigating with random...", False

    while True:
        dt = clock.tick(FPS) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: anim_play = not anim_play
                algo_keys = {pygame.K_r: 'random', pygame.K_h: 'hill_climbing', 
                            pygame.K_s: 'simulated_annealing', pygame.K_g: 'genetic_algorithm'}
                if event.key in algo_keys:
                    TEMP = 10
                    status, flash_shown = start_new_game(grid, drone, algo_keys[event.key]), False
            
            if event.type == pygame.MOUSEBUTTONDOWN and drone.reached_destination:
                if draw_restart_button(screen, font).collidepoint(pygame.mouse.get_pos()):
                    status, flash_shown = start_new_game(grid, drone, drone.algorithm), False

        if anim_play and not drone.reached_destination: drone.update(dt)
        
        if drone.reached_destination and not flash_shown:
            TEMP = 10
            draw_grid(screen, grid, drone.start, drone.destination)
            screen.blit(drone_image, drone_image.get_rect(center=drone.get_position()))
            flash = pygame.Surface((WIDTH, HEIGHT))
            flash.set_alpha(128)
            flash.fill(YELLOW)
            screen.blit(flash, (0, 0))
            pygame.display.flip()
            pygame.time.wait(500)
            status, flash_shown = "Destination reached! Click RESTART.", True
        
        draw_grid(screen, grid, drone.start, drone.destination)
        screen.blit(drone_image, drone_image.get_rect(center=drone.get_position()))
        draw_info(screen, font, status, len(drone.path)-1, drone.algorithm)
        if drone.reached_destination: draw_restart_button(screen, font)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()