"""
Gomoku AI Template
------------------
TODO Template for implementing different AI strategies:
    - Random Move
    - Monte Carlo (simple heuristic version)
    - Minimax
    - Alpha-Beta Pruning
"""

import sys
import math
import random
import copy

sys.setrecursionlimit(1500)
N = 15  # board size (15x15)


class GomokuAI:
    def __init__(self, depth=3):
        self.depth = depth
        self.boardMap = [[0 for _ in range(N)] for _ in range(N)]
        self.currentI = -1
        self.currentJ = -1
        self.boardValue = 0
        self.turn = 0
        self.lastPlayed = 0
        self.emptyCells = N * N
        self.nextBound = {}

    #######################################################
    # --- Basic utilities (already implemented) ---
    #######################################################
    def drawBoard(self):
        for i in range(N):
            for j in range(N):
                val = self.boardMap[i][j]
                print("x|" if val == 1 else "o|" if val == -1 else ".|", end=" ")
            print()
        print()

    def setState(self, i, j, state):
        assert state in (-1, 0, 1)
        self.boardMap[i][j] = state
        self.lastPlayed = state

    def childNodes(self, bound):
        for pos in sorted(bound.items(), key=lambda el: el[1], reverse=True):
            yield pos[0]

    def checkResult(self):
        if self.isFive(self.currentI, self.currentJ, self.lastPlayed):
            return self.lastPlayed
        elif self.emptyCells <= 0:
            return 0  # tie
        else:
            return None
        
    def getWinner(self):
        if self.checkResult() == 1:
            return "Black AI"
        if self.checkResult() == -1:
            return "White AI"
        return "None"

    def firstMove(self):
        """Place first stone in the center of the board."""
        self.currentI, self.currentJ = N // 2, N // 2
        self.setState(self.currentI, self.currentJ, 1)
        self.emptyCells -= 1
        if not self.nextBound:
            self.nextBound = {}
        self.updateBound(self.currentI, self.currentJ, self.nextBound)

    def updateBound(self, new_i, new_j, bound):
        bound.pop((new_i, new_j), None)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                ni, nj = new_i + dx, new_j + dy
                if 0 <= ni < N and 0 <= nj < N and self.boardMap[ni][nj] == 0:
                    bound[(ni, nj)] = bound.get((ni, nj), 0) + 1

    def isValid(self, i, j):
        return 0 <= i < N and 0 <= j < N and self.boardMap[i][j] == 0

    def countDirection(self, i, j, xdir, ydir, state):
        count = 0
        x, y = i + xdir, j + ydir
        while 0 <= x < N and 0 <= y < N and self.boardMap[x][y] == state:
            count += 1
            x += xdir
            y += ydir
        return count

    def isFive(self, i, j, state):
        if i < 0 or j < 0:
            return False
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            total = 1 + self.countDirection(i, j, dx, dy, state) + self.countDirection(i, j, -dx, -dy, state)
            if total >= 5:
                return True
        return False

    def evaluate(self, new_i, new_j, board_value, turn, bound):
        """Basic heuristic evaluation for connected stones."""
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1 + self.countDirection(new_i, new_j, dx, dy, turn) + self.countDirection(new_i, new_j, -dx, -dy, turn)
            if count >= 5:
                score += 100000
            elif count == 4:
                score += 10000
            elif count == 3:
                score += 1000
            elif count == 2:
                score += 100
        bonus = bound.get((new_i, new_j), 0) if bound is not None else 0
        return board_value + score * (1 if turn == 1 else -1) + 0.1 * bonus

    #######################################################
    # --- TODO: Implement the following strategies ---
    #######################################################

    def randomMove(self):
        """
        TODO: Select a random valid move.
        Steps:
          - Collect all empty cells on the board.
          - Randomly choose one of them.
          - Update self.currentI, self.currentJ.
        """
        self.currentI, self.currentJ = random.randint(0,14),random.randint(0,14)
        while not self.isValid(self.currentI,self.currentJ):
            self.currentI, self.currentJ = random.randint(0,14),random.randint(0,14)

    def monteCarloTreeSearch(self, board_value, bound):
        """
        TODO: Implement a simple Monte Carlo (heuristic) move selector.
        Hints:
          - Iterate over possible moves from 'bound'.
          - For each move:
              1. Temporarily place a stone.
              2. Evaluate it with self.evaluate().
              3. Undo the move.
          - Pick the move with the highest score.
        """
        new_places = list(self.childNodes(bound))
        if self.turn == 1:
            best_choice_point = -99999999
        if self.turn == -1:
            best_choice_point = 99999999
        best_choice = (self.currentI,self.currentJ)
        for new_i,new_j in new_places:
            eva = self.evaluate(new_i, new_j, board_value, self.turn, bound)
            if  (self.turn == 1 and eva > best_choice_point) or (self.turn == -1 and eva < best_choice_point):
                best_choice = (new_i,new_j)
                best_choice_point = eva
        self.currentI, self.currentJ = best_choice


    def minimax(self, depth, board_value, bound, maximizingPlayer):
        """
        TODO: Implement the minimax algorithm (no alpha-beta pruning).
        Hints:
          - Use recursion with alternating maximizing/minimizing players.
          - Return (i, j) of the best move.
          - Base case: depth == 0 or terminal (checkResult != None).
        """
        if depth == 0 or self.checkResult() != None:
            return board_value
        
        best_moves = list(self.childNodes(bound))
        # best_moves = best_moves[:len(best_moves) - 20]
        best_value_place = 0
        best_value = 0
        values = list()
        for (new_i,new_j) in best_moves:
            now_board_value = self.evaluate(new_i,new_j,board_value,maximizingPlayer,bound)
            self.boardMap[new_i][new_j] = maximizingPlayer
            new_bound = bound.copy()
            self.updateBound(new_i,new_j,new_bound)
            values.append(self.minimax(depth-1,now_board_value,new_bound,maximizingPlayer * -1 ))
            self.boardMap[new_i][new_j] = 0

        if maximizingPlayer == 1 : 
            best_value_place = best_moves[values.index(max(values))]
            best_value = max(values)
        elif maximizingPlayer == -1 : 
            best_value_place = best_moves[values.index(min(values))]
            best_value = min(values)
        if depth == self.depth :
            self.currentI , self.currentJ = best_value_place
            return 

        return best_value
        

    def alphaBetaPruning(self, depth, board_value, bound, alpha, beta, maximizingPlayer):
        """
        TODO: Implement minimax with alpha-beta pruning.
        Hints:
          - Same structure as minimax but include alpha/beta checks.
          - Prune branches where beta <= alpha.
          - Keep track of the best move found at the top depth.
        """
        if depth == 0 or self.checkResult() != None:
            return alpha , beta ,board_value
        
        best_moves = list(self.childNodes(bound))
        # best_moves = best_moves[:len(best_moves) - 20]
        best_value_place = 0
        best_value = 0
        values = list()
        for (new_i,new_j) in best_moves:
            now_board_value = round(self.evaluate(new_i,new_j,board_value,maximizingPlayer,bound),2)
            self.boardMap[new_i][new_j] = maximizingPlayer
            new_bound = bound.copy()
            self.updateBound(new_i,new_j,new_bound)
            alpha, beta , v = self.alphaBetaPruning(depth-1,now_board_value,new_bound,alpha,beta,maximizingPlayer * -1 )
            if maximizingPlayer == -1 :
                if v < alpha :
                    self.boardMap[new_i][new_j] = 0
                    print(f"v : {v},alpha : {alpha}")
                    return alpha , beta , v
                alpha = max(v,alpha)

            if maximizingPlayer == 1:
                if v > beta :
                    self.boardMap[new_i][new_j] = 0
                    print(f"v : {v},beta : {beta}")
                    return alpha , beta , v
                beta = min(v,beta)

            values.append(v)
            self.boardMap[new_i][new_j] = 0

        if maximizingPlayer == 1 : 
            best_value_place = best_moves[values.index(max(values))]
            best_value = max(values)

        elif maximizingPlayer == -1 : 
            best_value_place = best_moves[values.index(min(values))]
            best_value = min(values)
            
        if depth == self.depth :
            print(f"best_value_place:{best_value_place}")
            self.currentI , self.currentJ = best_value_place
            return 

        return alpha , beta , best_value
