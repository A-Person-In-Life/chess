WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 8
BACKGROUND_COLORS = [(109, 129, 150), (210, 180, 140), (100, 100, 100)]
ROWS, COLS = 8, 8

from game_logic import BoardState, GameLogic
import pygame

class Board:
    def __init__(self):
        self.board_state = BoardState()
        self.grid = self.board_state.grid
        self.load_images()

    def load_images(self):
        self.images = {
            "PawnW" : pygame.image.load("images/white_pawn.png"),
            "PawnB" : pygame.image.load("images/black_pawn.png"),
            "BishopW": pygame.image.load("images/white_bishop.png"),
            "BishopB": pygame.image.load("images/black_bishop.png"),
            "RookW": pygame.image.load("images/white_rook.png"),
            "RookB": pygame.image.load("images/black_rook.png"),
            "QueenW": pygame.image.load("images/white_queen.png"),
            "QueenB": pygame.image.load("images/black_queen.png"),
            "KnightW": pygame.image.load("images/white_knight.png"),
            "KnightB": pygame.image.load("images/black_knight.png"),
            "KingW": pygame.image.load("images/white_king.png"),
            "KingB": pygame.image.load("images/black_king.png"),
            }

    def draw(self, screen):
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece:
                    color = "W" if piece.color == "white" else "B"
                    key = piece.name + color
                    screen.blit(self.images[key], (col * CELL_SIZE, row * CELL_SIZE))

class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.gamelogic = GameLogic()
        self.selected_piece = None
        self.turn = "white"
        
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(self.screen, BACKGROUND_COLORS[(row + col) % 2], (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                
    def draw(self):
        self.draw_board()
        self.draw_possible_moves()
        self.board.draw(self.screen)

    def draw_possible_moves(self):
        if self.selected_piece != None:
            moves = self.selected_piece.get_moves(self.board)
            for y,x in moves:
                pygame.draw.circle(self.screen,BACKGROUND_COLORS[2],((x*CELL_SIZE)+CELL_SIZE//2,(y*CELL_SIZE)+CELL_SIZE//2),40)

    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // CELL_SIZE
                    row = event.pos[1] // CELL_SIZE 
                    if self.selected_piece is None:
                        if self.board.grid[row][col] is not None and self.board.grid[row][col].color == self.turn:
                            self.selected_piece = self.board.grid[row][col]
                            print(self.board.grid[row][col])
                    else:
                        if self.board.board_state.move(self.selected_piece,row,col):
                            self.turn = "white" if self.turn == "black" else "white"
                            self.selected_piece = None                   
                    
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.loop()