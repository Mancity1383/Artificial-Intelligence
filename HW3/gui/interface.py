import pygame
import source.utils as utils

class GameUI:
    def __init__(self, ai):
        pygame.init()
        self.ai = ai
        self.size = 640
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Gomoku AI vs AI")
        self.board = self.createBoard()
        self.buttonSurf = pygame.Surface((100, 40))
        self.font = pygame.font.SysFont('arial', 20)
        self.result_font = pygame.font.SysFont('arial', 40, bold=True)

    def createBoard(self):
        """Draw the Gomoku board background."""
        board = pygame.Surface((self.size, self.size))
        board.fill((230, 200, 150))  # Light wood color
        grid_size = utils.N
        margin = 40
        cell_size = (self.size - 2 * margin) / (grid_size - 1)

        for i in range(grid_size):
            pygame.draw.line(board, (0, 0, 0),
                             (margin, margin + i * cell_size),
                             (self.size - margin, margin + i * cell_size))
            pygame.draw.line(board, (0, 0, 0),
                             (margin + i * cell_size, margin),
                             (margin + i * cell_size, self.size - margin))
        return board

    def drawPiece(self, color, i, j):
        """Draw a black or white stone on the board."""
        grid_size = utils.N
        margin = 40
        cell_size = (self.size - 2 * margin) / (grid_size - 1)
        center_x = int(margin + j * cell_size)
        center_y = int(margin + i * cell_size)
        radius = int(cell_size / 2.5)

        pygame.draw.circle(self.screen,
                        (0, 0, 0) if color == 'black' else (255, 255, 255),
                        (center_x, center_y), radius)
        pygame.draw.circle(self.screen, (0, 0, 0), (center_x, center_y), radius, 1)
        pygame.display.update()

    def drawButtons(self, button, surface):
        """Draw multiple buttons (used in strategy selection)."""
        button.draw(surface)

    def drawButton(self, button, surface):
        """Draw a single button, e.g., when highlighting selected one."""
        button.draw(surface)

    def drawResult(self, tie=False):
        """Show the final result screen."""
        self.screen.fill((240, 240, 240))
        if tie:
            text = self.result_font.render("It's a tie!", True, (50, 50, 50))
        else:
            winner = self.ai.getWinner()
            text = self.result_font.render(f"{winner} wins!", True, (0, 100, 0))
        self.screen.blit(text, (self.size // 2 - text.get_width() // 2,
                                self.size // 2 - text.get_height() // 2))
        pygame.display.update()

    def restartChoice(self, mouse_pos):
        """Handle click to restart (optional for extension)."""
        print("Restart not implemented yet.")
