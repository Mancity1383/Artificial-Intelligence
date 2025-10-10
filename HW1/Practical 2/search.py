"""
search.py

Students must implement TODO sections.
Includes: BFS, DFS, UCS, A* (with Manhattan & Euclidean heuristics).
"""
from collections import deque
import heapq
import math

def heuristic_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristic_euclidean(a, b):
    return math.sqrt(abs(a[0] - b[0]) ** 2 + abs(a[1] - b[1]) ** 2)

# ---------------------
# BFS
# ---------------------
def breadth_first_search(start, goal, neighbors_fn, grid):
    block_counter = 0
    checked_list = []
    queue = deque()
    path = []
    visited = dict()
    visited[start] = None
    queue.append(start)
    node = start
    while queue:
        node = queue.popleft()
        if node == goal:
            break
        x = node[0]
        y = node[1]
        for blocks in neighbors_fn(node):
            if blocks not in visited:
                if blocks not in checked_list: checked_list.append(blocks)
                block_counter +=1
                grid[x][y] = 2
                visited[blocks] = (x, y)
                queue.append(blocks)

    while node is not None:
        path.append(node)
        grid[node[0]][node[1]] = 3
        node = visited[node]
    path.reverse()
    print(f'Visited Blocks : {len(checked_list)}')

    return path



# ---------------------
# DFS
# ---------------------
def depth_first_search(start, goal, neighbors_fn,grid):
    block_counter = 0
    checked_list = []
    queue = deque()
    path = []
    visited = dict()
    visited[start] = None
    queue.append(start)
    node = start
    while queue:
        node = queue.pop()

        if node == goal:
            break
        x = node[0]
        y = node[1]
        for blocks in neighbors_fn(node):
            if blocks not in visited:
                if blocks not in checked_list: checked_list.append(blocks)
                block_counter += 1
                grid[x][y] = 2
                visited[blocks] = (x, y)
                queue.append(blocks)

    while node is not None:
        path.append(node)
        grid[node[0]][node[1]] = 3
        node = visited[node]
    path.reverse()
    print(f'Visited Blocks : {len(checked_list)}')

    return path


# ---------------------
# UCS
# ---------------------
def uniform_cost_search(start, goal, neighbors_fn,grid):
    block_counter = 0
    checked_list = []
    heap = []
    path = []
    visited = {}
    visited[start] = (None, 0)
    heapq.heappush(heap, (0, start)) 
    
    while heap :
        node = heapq.heappop(heap)
        x,y = node[1][0],node[1][1]
        grid[x][y] = 2
        weight = node[0]
        if node[1] == goal:
            break
        for blocks in neighbors_fn(node[1]):
            cost = blocks[1]+weight
            if blocks[0] not in visited or cost  < visited[blocks[0]][1]:
                if blocks not in checked_list: checked_list.append(blocks)
                block_counter += 1
                visited[blocks[0]] = (node[1],cost)
                heapq.heappush(heap,(cost,blocks[0]))   

    node = goal
    while node is not None:
        path.append(node)
        grid[node[0]][node[1]] = 3
        node = visited.get(node, (None,))[0]
    path.reverse()
    print(f'Visited Blocks : {len(checked_list)}')
    print(f'Weight : {weight}')

    return path


# ---------------------
# A* Search
# ---------------------
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    return math.sqrt(abs(a[0] - b[0]) ** 2 + abs(a[1] - b[1]) ** 2)

def a_star_search(start, goal, neighbors_fn,heuristic,grid):
    block_counter = 0
    checked_list = []
    heap = []
    path = []
    visited = {}
    visited[start] = (None, 0)
    heapq.heappush(heap, (0, start)) 
    
    while heap :
        node = heapq.heappop(heap)
        x,y = node[1][0],node[1][1]
        grid[x][y] = 2
        weight = visited[node[1]][1]
        if node[1] == goal:
            break
        for blocks in neighbors_fn(node[1]):
            h = 0
            if heuristic == "manhattan":
                h = manhattan(blocks[0],goal)
            elif heuristic == "euclidean" :
                h = euclidean(blocks[0],goal)
            
            cost = blocks[1]+ weight
            if blocks[0] not in visited or cost < visited[blocks[0]][1]:
                if blocks not in checked_list: checked_list.append(blocks)
                block_counter += 1
                visited[blocks[0]] = (node[1],cost)
                heapq.heappush(heap,(cost+h,blocks[0]))   

    node = goal
    weight = visited[node][1]
    while node is not None:
        path.append(node)
        grid[node[0]][node[1]] = 3
        node = visited.get(node, (None,))[0]
    path.reverse()
    print(f'Visited Blocks : {len(checked_list)}')
    print(f'Weight : {weight}')

    return path