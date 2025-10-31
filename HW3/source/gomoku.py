import math
import time
import pygame
from source.AI import *
from gui.interface import *
import source.utils as utils 

pygame.init()

def ai_move(ai, strategy="alphabeta"):
    """AI move based on chosen strategy: minimax or alpha-beta pruning."""
    start_time = time.time()

    if strategy == "minimax":
        ai.minimax(ai.depth, ai.boardValue, ai.nextBound, True)
    elif strategy == "alphabeta":
        ai.alphaBetaPruning(ai.depth, ai.boardValue, ai.nextBound, -math.inf, math.inf, True)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    end_time = time.time()
    print(f'[{strategy}] finished in: {end_time - start_time:.3f}s')

    # If AI move is valid, apply it
    if ai.isValid(ai.currentI, ai.currentJ):
        move_i, move_j = ai.currentI, ai.currentJ
    else:
        print('Error: i and j not valid. Using best bound fallback.')
        bound_sorted = sorted(ai.nextBound.items(), key=lambda el: el[1], reverse=True)
        move_i, move_j = bound_sorted[0][0]
        ai.currentI, ai.currentJ = move_i, move_j

    ai.updateBound(move_i, move_j, ai.nextBound)
    print(f'AI Move -> ({move_i}, {move_j})')
    return move_i, move_j


def check_human_move(ai, mouse_pos):
    """Check if human move is valid and update the board."""
    move_i, move_j = utils.pos_pixel2map(mouse_pos[0], mouse_pos[1])
    
    if ai.isValid(move_i, move_j):
        ai.boardValue = ai.evaluate(move_i, move_j, ai.boardValue, -1, ai.nextBound)
        ai.setState(move_i, move_j, -1)
        ai.updateBound(move_i, move_j, ai.nextBound)
        return move_i, move_j
    return None


def check_results(ui, result):
    """Display result (win or tie) and allow restart."""
    if result == 0:
        print("It's a tie!")
        ui.drawResult(tie=True)
    else:
        ui.drawResult()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            ui.restartChoice(pygame.mouse.get_pos())
