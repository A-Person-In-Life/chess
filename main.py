import pygame

WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 8
BACKGROUND_COLORS = [(109, 129, 150), (210, 180, 140)]


class Piece:
    def __init__(self, name, row, col, color, image):
        self.name = name
        self.image = image
        self.row = row
        self.col = col
        self.color = color

    def moveLogic(self, originCol, originRow, moveCol, moveRow):
        rowDiff = abs(originRow - moveRow)
        colDiff = abs(originCol - moveCol)

        if self.name == "pawn":
            if self.color == "white":
                rowDiff = originRow - moveRow
            elif self.color == "black":
                rowDiff = (originRow - moveRow) * -1
            
            if originRow == 1 or originRow == 6:
                if (rowDiff == 1 or rowDiff == 2) and colDiff == 0:
                    return True
            else:
                if rowDiff == 1 and colDiff == 0:
                    return True
        
        if self.name == "rook":
            if rowDiff == 0 or colDiff == 0:
                return True
        
        if self.name == "bishop":
            if rowDiff == colDiff:
                return True
        
        if self.name == "queen":
            if rowDiff == 0 or colDiff == 0 or rowDiff == colDiff:
                return True
        
        if self.name == "king":
            if rowDiff <= 1 and colDiff <= 1:
                return True
        
        return False

    def draw(self, screen):
        screen.blit(self.image, (self.col * CELL_SIZE, self.row * CELL_SIZE))

class Board:
    def __init__(self):
        self.grid = [[None for i in range(8)] for j in range(8)]
        self.setup()
        
    def setup(self):
        order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]

        for col, name in enumerate(order):
            self.grid[0][col] = Piece(name, 0, col, "black", pygame.image.load(f"images/black_{name}.png"))
            self.grid[1][col] = Piece("pawn", 1, col, "black", pygame.image.load(f"images/black_pawn.png"))

            self.grid[6][col] = Piece("pawn", 6, col, "white", pygame.image.load(f"images/white_pawn.png"))
            self.grid[7][col] = Piece(name, 7, col, "white", pygame.image.load(f"images/white_{name}.png"))

    def move(self, originCol, originRow, moveCol, moveRow):
        piece = self.grid[originRow][originCol]
        piece.row = moveRow
        piece.col = moveCol
        
        self.grid[originRow][originCol] = None
        self.grid[moveRow][moveCol] = piece

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

    def handleMoves(self, row, col):
        if self.board.grid[row][col] != None:
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        moveCol = event.pos[0] // CELL_SIZE
                        moveRow = event.pos[1] // CELL_SIZE
                        
                        if not self.board.grid[moveRow][moveCol] == None:
                            if self.board.grid[moveRow][moveCol].color == self.board.grid[row][col].color:
                                waiting = False
                                continue
                            
                        if self.board.grid[row][col].moveLogic(col, row, moveCol, moveRow):
                            self.board.move(col, row, moveCol, moveRow)
                            waiting = False
                        else:
                            waiting = False
                            
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        waiting = False

if __name__ == "__main__":
    game = Game()
    game.loop()