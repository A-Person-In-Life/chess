import pygame

#task is to seperate the logic and gamestates from the pygame drawing aspect so that the AI will never even touch pygame when training.


WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 8
BACKGROUND_COLORS = [(109, 129, 150), (210, 180, 140), (100, 100, 100)]
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
    
    def handleSlidingMoves(self, directions, board):
        moves = []
        row, col = self.row, self.col

        for xDir, yDir in directions:
            step = 1
            blocked = False
            while not blocked:
                newRow = row + xDir * step
                newCol = col + yDir * step

                if not inside(newRow, newCol):
                    blocked = True
                else:
                    target = board.grid[newRow][newCol]

                    if target is None:
                        moves.append((newRow, newCol))
                    else:
                        if target.color != self.color:
                            moves.append((newRow, newCol))
                        blocked = True
                    step += 1
        return moves
    
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
        # captures
        for colDiff in (-1, 1):
            newRow, newCol = row + side, col + colDiff
            if inside(newRow, newCol) and board.grid[newRow][newCol] != None:
                if self.color != board.grid[newRow][newCol].color:
                    moves.append((newRow, newCol))
        return moves
    
#try, in another file, to refactor the movement system to hold all possible moves for each piece efficiently and find an algorithm to update those moves only when nec
class King(Piece):
    def get_moves(self,board):
        moves = []
        row, col = self.row, self.col
        directions = [(1,0),(1,1),(0,1),(-1,1),(-1,-1),(-1,0),(0,-1),(1,-1)]
        for xDir, yDir in directions:
            moveRow = row + 1 * xDir
            moveCol = col + 1 * yDir
            if inside(moveRow,moveCol):
                target = board.grid[moveRow][moveCol]
                if not self.inCheck(target, board, enemyMove):
                    if target == None:
                        moves.append((moveRow, moveCol))
                    else:
                        if target.color != self.color:
                            moves.append((moveRow, moveCol))
        return moves
    
    def inCheck(self, target, board):
        pass

class Bishop(Piece):
    def get_moves(self, board):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self.handleSlidingMoves(directions, board)
    
class Rook(Piece):
    def get_moves(self, board):
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        return self.handleSlidingMoves(directions, board)

class Queen(Piece):
    def get_moves(self, board):
        directions = [(-1, -1),(-1, 0),(-1, 1),(0, -1),(0, 1),(1, -1),(1, 0),(1, 1)]
        return self.handleSlidingMoves(directions, board)

class Knight(Piece):
    def get_moves(self, board):
        moves = []
        row, col = self.row, self.col
        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for rowDiff, colDiff in knightMoves:
            moveRow = row + rowDiff
            moveCol = col + colDiff
            if inside(moveRow,moveCol):
                target = board.grid[moveRow][moveCol]
                if target == None:
                    moves.append((moveRow, moveCol))
                else:
                    if target.color != self.color:
                        moves.append((moveRow, moveCol))
        return moves

class Board:
    def __init__(self):
        self.grid = [[None for i in range(8)] for j in range(8)]
        self.load_images()
        self.setup()

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
            "KingB": pygame.image.load("images/black_king.png")
        }
    def setup(self):

        self.grid[0][0] = Rook(0,0,"black",self.images["RookB"])
        self.grid[0][7] = Rook(0,7,"black",self.images["RookB"])
        self.grid[7][0] = Rook(7,0,"white",self.images["RookW"])
        self.grid[7][7] = Rook(7,7,"white",self.images["RookW"])

        self.grid[0][2] = Bishop(0,2,"black",self.images["BishopB"])
        self.grid[0][5] = Bishop(0,5,"black",self.images["BishopB"])
        self.grid[7][2] = Bishop(7,2,"white",self.images["BishopW"])
        self.grid[7][5] = Bishop(7,5,"white",self.images["BishopW"])

        self.grid[0][4] = Queen(0,4,"black",self.images["QueenB"])
        self.grid[7][4] = Queen(7,4,"white",self.images["QueenW"])

        self.grid[0][3] = King(0,3,"black",self.images["KingB"])

        self.grid[0][1] = Knight(0,1,"black",self.images["KnightB"])
        self.grid[0][6] = Knight(0,6,"black",self.images["KnightB"])
        self.grid[7][1] = Knight(7,1,"white",self.images["KnightW"])
        self.grid[7][6] = Knight(7,6,"white",self.images["KnightW"])
                                
        for c in range(COLS):
            self.grid[1][c] = Pawn(1, c, "black", self.images["PawnB"])
            self.grid[6][c] = Pawn(6, c, "white", self.images["PawnW"])

    #what data type is piece in this context and why is it a problem
    #an object? But that should work right?
    def move(self, piece, destRow, destCol):
        # Ensure we call get_moves with the board and check membership
        if (destRow, destCol) not in piece.get_moves(self):
            return False
        self.grid[piece.row][piece.col] = None    
        piece.row, piece.col = destRow, destCol
        self.grid[destRow][destCol] = piece#add later for AI
        return True

    def draw(self, screen):
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece:
                    piece.draw(screen)

import pygame

class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.selected_piece = None
        self.board = Board()
        self.turn = "white"
        
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(self.screen, BACKGROUND_COLORS[(row + col) % 2], (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                
    def draw_possible_moves(self):
        if self.selected_piece != None:
            moves = self.selected_piece.get_moves(self.board)
            for y,x in moves:
                pygame.draw.circle(self.screen,BACKGROUND_COLORS[2],((x*CELL_SIZE)+CELL_SIZE//2,(y*CELL_SIZE)+CELL_SIZE//2),40)
                
    def draw(self):
        self.draw_board()
        self.draw_possible_moves()
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
                    if self.selected_piece is None:
                        if self.board.grid[row][col] is not None and self.board.grid[row][col].color == self.turn:
                            self.selected_piece = self.board.grid[row][col]
                            print(self.board.grid[row][col])
                    else:
                        if self.board.move(self.selected_piece,row,col):
                            self.turn = "white" if self.turn == "black" else "white"
                            self.selected_piece = None
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

game = Game()
game.loop()