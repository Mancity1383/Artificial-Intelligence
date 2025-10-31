# play.py (fixed)
from gui.interface import *
from source.AI import *
from gui.button import Button
import source.utils as utils
import source.gomoku as gomoku
import pygame
import random
import time

pygame.init()

def startGame():
    pygame.init()
    # Use a single shared GomokuAI for the whole game
    ai = GomokuAI()
    game = GameUI(ai)

    # Strategy options (1..4)
    strategies = ["Random", "Minimax", "AlphaBeta", "MonteCarlo"]
    buttons_black = []
    buttons_white = []

    # Draw initial selection screen
    game.screen.fill((245, 245, 245))
    title_font = pygame.font.SysFont('arial', 30, bold=True)
    text_font = pygame.font.SysFont('arial', 20)

    title = title_font.render("Select AI Strategy", True, (0, 0, 0))
    game.screen.blit(title, (170, 50))

    black_text = text_font.render("Black Player:", True, (0, 0, 0))
    game.screen.blit(black_text, (100, 120))
    white_text = text_font.render("White Player:", True, (0, 0, 0))
    game.screen.blit(white_text, (100, 250))

    # Create buttons for Black and White player strategies
    x_start = 250
    for idx, label in enumerate(strategies):
        btn_b = Button(game.buttonSurf, x_start + idx * 100, 120, label, 18)
        buttons_black.append(btn_b)
        btn_w = Button(game.buttonSurf, x_start + idx * 100, 250, label, 18)
        buttons_white.append(btn_w)

    # Draw all buttons
    for btn in buttons_black + buttons_white:
        game.drawButtons(btn, game.screen)

    pygame.display.update()

    # Wait for player to choose both strategies
    black_method, white_method = None, None
    choosing = True
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()

                for i, btn in enumerate(buttons_black):
                    if btn.rect.collidepoint(mouse_pos):
                        black_method = i + 1
                        print("Black selected:", strategies[i])
                        # highlight selected
                        for b in buttons_black:
                            b.text = b.button_font.render(b.text_input, True, "white")
                        btn.text = btn.button_font.render(btn.text_input, True, "yellow")
                        game.drawButton(btn, game.screen)
                        pygame.display.update()

                for i, btn in enumerate(buttons_white):
                    if btn.rect.collidepoint(mouse_pos):
                        white_method = i + 1
                        print("White selected:", strategies[i])
                        for b in buttons_white:
                            b.text = b.button_font.render(b.text_input, True, "white")
                        btn.text = btn.button_font.render(btn.text_input, True, "yellow")
                        game.drawButton(btn, game.screen)
                        pygame.display.update()

                if black_method and white_method:
                    choosing = False

    # Clear the screen and draw the game board
    game.screen.blit(game.board, (0, 0))
    pygame.display.update()

    # Black always starts first
    ai.turn = 1

    # Black's first move (center)
    if ai.turn == 1:
        ai.firstMove()
        # ensure bound updated (firstMove already does)
        game.drawPiece('black', ai.currentI, ai.currentJ)
        pygame.display.update()
        ai.turn *= -1

    # Start the main AI-vs-AI loop using the shared 'ai'
    main(game, ai, black_method, white_method)

    # End game: show result
    if ai.checkResult() is not None:
        last_screen = game.screen.copy()
        game.screen.blit(last_screen, (0, 0))
        game.drawResult()
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()


def ai_move_with_strategy(ai, strategy_id):
    """Decide AI move based on chosen strategy. Returns valid (i,j)."""
    # Random
    if strategy_id == 1:
        ai.randomMove()
        move_i, move_j = ai.currentI, ai.currentJ

    elif strategy_id == 2:
        # Minimax: it will set ai.currentI/currentJ
        ai.minimax(ai.depth, ai.boardValue, ai.nextBound, True)
        move_i, move_j = ai.currentI, ai.currentJ

    elif strategy_id == 3:
        # Alpha-Beta
        ai.alphaBetaPruning(ai.depth, ai.boardValue, ai.nextBound, -float('inf'), float('inf'), True)
        move_i, move_j = ai.currentI, ai.currentJ

    elif strategy_id == 4:
        # Monte Carlo (simple selector)
        ai.monteCarloTreeSearch(ai.boardValue, ai.nextBound)
        move_i, move_j = ai.currentI, ai.currentJ

    # Safety: if selected move is invalid (shouldn't happen), pick a valid one
    if not ai.isValid(move_i, move_j):
        valid_moves = [(i, j) for i in range(N) for j in range(N) if ai.boardMap[i][j] == 0]
        if valid_moves:
            move_i, move_j = random.choice(valid_moves)
        else:
            move_i, move_j = -1, -1

    return move_i, move_j


def main(game, ai, black_method, white_method):
    """Main gameplay loop for AI vs AI using a single shared GomokuAI instance.
       Tracks time per move and overall game duration."""
    pygame.init()
    end = False

    move_times = {1: [], -1: []}   # store duration of each move per player
    move_counts = {1: 0, -1: 0}   # count moves per player

    # Start total game timer
    total_start = time.perf_counter()   

    while not end:
        turn = ai.turn
        color = 'black' if turn == 1 else 'white'
        method = black_method if turn == 1 else white_method

        # Measure time for this move
        move_start = time.perf_counter()
        move_i, move_j = ai_move_with_strategy(ai, method)
        move_end = time.perf_counter()

        # Convert to milliseconds and store
        move_duration_ms = (move_end - move_start) * 1000
        move_times[turn].append(move_duration_ms)
        move_counts[turn] += 1

        # Apply move and update board
        if move_i != -1 and ai.isValid(move_i, move_j):
            ai.setState(move_i, move_j, turn)
            ai.currentI, ai.currentJ = move_i, move_j
            ai.emptyCells -= 1
            ai.updateBound(move_i, move_j, ai.nextBound)
            game.drawPiece(color, move_i, move_j)
            pygame.display.update()
            pygame.time.wait(300)  # small delay for visualization
        else:
            print("Selected invalid move, skipping turn.", move_i, move_j)

        # Check for winner
        result = ai.checkResult()
        if result is not None:
            print("Winner:", ai.getWinner())
            end = True
            break

        # Switch turn
        ai.turn *= -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

    # End of game: calculate total duration
    total_end = time.perf_counter()
    total_duration_ms = (total_end - total_start) * 1000

    # Pause briefly before showing summary
    pygame.time.wait(1500)

    # Display summary on screen
    game.screen.fill((245, 245, 245))
    font = pygame.font.SysFont('arial', 22, bold=True)
    y_start = 50

    # Calculate average move times
    black_avg_ms = (sum(move_times[1])/len(move_times[1])) if move_times[1] else 0
    white_avg_ms = (sum(move_times[-1])/len(move_times[-1])) if move_times[-1] else 0

    # Prepare summary lines
    lines = [
        f"Game Summary:",
        f"Black moves: {move_counts[1]}, avg time: {black_avg_ms:.4f} ms",
        f"White moves: {move_counts[-1]}, avg time: {white_avg_ms:.4f} ms",
        f"Winner: {ai.getWinner()}",
        f"Total game duration: {total_duration_ms:.4f} ms"
    ]

    # Render each line on the screen
    for line in lines:
        text_surf = font.render(line, True, (0, 0, 0))
        game.screen.blit(text_surf, (50, y_start))
        y_start += 40

    pygame.display.update()
    pygame.time.wait(4000)  # keep summary on screen for 4 seconds


    # Draw final result as usual
    game.drawResult()


if __name__ == '__main__':
    startGame()
