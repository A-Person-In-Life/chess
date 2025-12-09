import pygame

WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 8
BACKGROUND_COLORS = [(109, 129, 150), (210, 180, 140)]
ROWS, COLS = 8, 8

def inside(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7

class Piece:
    def __init__(self, row, col, color, image):
        self.image = image
        self.row = row
        self.col = col
        self.color = color

    def draw(self, screen):
        screen.blit(self.image, (self.col * CELL_SIZE, self.row * CELL_SIZE))

class Pawn(Piece):
    def get_moves(self, board):
        moves = []
        side = -1 if self.color == "white" else 1
        row, col = self.row, self.col
        #one row forward
        if inside(row+side, col) and board.grid[row+side][col] == None: 
            moves.append((row+side,col))
            start_row = 6 if self.color == "white" else 1
            if row == start_row: #two rows forward
                if board.grid[row+(2*side)][col] == None:
                    moves.append((row+(2*side),col))
        #captures
        for colDiff in (-1, 1):
            newRow, newCol = row + side, col + colDiff
            if inside(newRow, newCol) and board.grid[newRow][newCol] != None:
                if self.color != board.grid[newRow][newCol].color:
                    moves.append(newRow, newCol)
        return moves

class Board:
    def __init__(self):
        self.grid = [[None for i in range(8)] for j in range(8)]
        self.load_images()
        self.setup()

    def load_images(self):
        self.images = {
            "PawnW" : pygame.image.load("images/white_pawn.png"),
            "PawnB" : pygame.image.load("images/black_pawn.png")
        }
    def setup(self):

        for c in range(COLS):
            self.grid[1][c] = Pawn(1, c, "black", self.images["PawnB"])
            self.grid[6][c] = Pawn(6, c, "white", self.images["PawnW"])
    #what data type is piece in this context and why is it a problem
    def move(self, piece, destRow, destCol):
        if (destRow, destCol) in piece.get_moves():
            self.grid[piece.row][piece.col] = None
            piece.row, piece.col = destRow, destCol
            self.grid[destRow][destCol] = self.grid[piece.row][piece.col]
            

    def draw(self, screen):
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece:
                    piece.draw(screen)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = Board()
        
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(self.screen, BACKGROUND_COLORS[(row + col) % 2], (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    def draw(self):
        self.draw_board()
        self.board.draw(self.screen)

    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // CELL_SIZE
                    row = event.pos[1] // CELL_SIZE
                    self.handleMoves(row, col)
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
    
    def handleMoves():
        pass


if __name__ == "__main__":
    game = Game()
    game.loop()