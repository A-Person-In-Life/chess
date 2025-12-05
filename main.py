import pygame

WIDTH, HEIGHT = 800,800
CELL_SIZE = WIDTH // 8
BACKGROUND_COLORS = [(109,129,150),(210,180,140)]


class Piece:
    def __init__(self, name, row, col, color, image):
        self.name = name
        self.image = image
        self.row = row
        self.col = col
        self.color = color

    def moveLogic(self, orginCol, orginRow, moveCol, moveRow):
        print("logic started")
        rowDiff = abs(orginRow - moveRow)
        colDiff = abs(orginCol - moveCol)

        if self.name == "pawn":
            print("is pawn")
            if orginRow == 1 or orginRow == 6:
                if rowDiff == 1 or rowDiff == 2 and colDiff == 0:
                    return True
            else:
                if rowDiff == 1 and colDiff == 0:
                    return True
        
        if self.name == "rook":
            pass

    def draw(self, screen):
        screen.blit(self.image, (self.col*CELL_SIZE, self.row*CELL_SIZE))
        

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

    def move(self, orginCol, orginRow, moveCol, moveRow):
        piece = self.grid[orginCol][orginRow]
        piece.row, piece.col = moveRow, moveCol
        
        self.grid[moveRow][moveCol] = None
        self.grid[orginRow][orginCol] = None
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
                pygame.draw.rect(self.screen,BACKGROUND_COLORS[(row+col)%2],(row*CELL_SIZE,col*CELL_SIZE,CELL_SIZE,CELL_SIZE))
    
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
                    col = event.pos[0] // 100
                    row = event.pos[1] // 100
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
                        moveRow = event.pos[0] // 100
                        moveCol = event.pos[1] // 100
                        if self.board.grid[moveCol][moveRow]:
                            if not self.board.grid[moveCol][moveRow].color == self.board.grid[row][col].color:
                                continue
                        if self.board.grid[row][col].moveLogic(row,col,moveCol,moveRow):
                            self.board.move(row, col, moveRow, moveCol)
                            waiting = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        waiting = False

if __name__ == "__main__":
    game = Game()
    game.loop()