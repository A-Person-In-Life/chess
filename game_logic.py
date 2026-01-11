def inside(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7

class Piece:
    def __init__(self, row, col, color, name):
        self.name = name
        self.row = row
        self.col = col
        self.color = color
    
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
        if inside(row+side, col) and board.grid[row+side][col] == None: 
            moves.append((row+side,col))
            start_row = 6 if self.color == "white" else 1
            if row == start_row:
                if board.grid[row+(2*side)][col] == None:
                    moves.append((row+(2*side),col))
        for colDiff in (-1, 1):
            newRow, newCol = row + side, col + colDiff
            if inside(newRow, newCol) and board.grid[newRow][newCol] != None:
                if self.color != board.grid[newRow][newCol].color:
                    moves.append((newRow, newCol))
        return moves
    
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

class King(Piece):
    def get_moves(self, board):
        moves = []
        row, col = self.row, self.col
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, -1), (-1, 0), (0, -1), (1, -1)]
        
        for xDir, yDir in directions:
            moveRow = row + 1 * xDir
            moveCol = col + 1 * yDir
            if inside(moveRow, moveCol):
                if not self.inCheck(board):
                    target = board.grid[moveRow][moveCol]
                    if target == None:
                        moves.append((moveRow, moveCol))
                    else:
                        if target.color != self.color:
                            moves.append((moveRow, moveCol))
                else: return True
        return moves
    
    def inCheck(self, board):
        
        for row in range(8):
            for col in range(8):
                piece = board.grid[row][col]
                if piece.color != self.color:
                    if (self.row, self.col) in piece.get_moves(board):
                        return True
        return False

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


class BoardState:
    def __init__(self):
        self.grid = [[None for i in range(8)] for j in range(8)]
        self.turn = "white"
        self.setup()
    
    def setup(self):

        self.grid[0][0] = Rook(0,0,"black","Rook")
        self.grid[0][7] = Rook(0,7,"black","Rook")
        self.grid[7][0] = Rook(7,0,"white","Rook")
        self.grid[7][7] = Rook(7,7,"white","Rook")

        self.grid[0][2] = Bishop(0,2,"black","Bishop")
        self.grid[0][5] = Bishop(0,5,"black","Bishop")
        self.grid[7][2] = Bishop(7,2,"white","Bishop")
        self.grid[7][5] = Bishop(7,5,"white","Bishop")

        self.grid[0][3] = King(0,3,"black","King")
        self.grid[7][3] = King(7,3,"white","King")

        self.grid[0][4] = Queen(0,4,"black","Queen")
        self.grid[7][4] = Queen(7,4,"white","Queen")

        self.grid[0][3] = King(0,3,"black","King")

        self.grid[0][1] = Knight(0,1,"black","Knight")
        self.grid[0][6] = Knight(0,6,"black","Knight")
        self.grid[7][1] = Knight(7,1,"white","Knight")
        self.grid[7][6] = Knight(7,6,"white","Knight")
                                
        for c in range(8):
            self.grid[1][c] = Pawn(1, c, "black", "Pawn")
            self.grid[6][c] = Pawn(6, c, "white", "Pawn")
    
    def move(self, piece, destRow, destCol):
        if (destRow, destCol) not in piece.get_moves(self):
            return False
        self.grid[piece.row][piece.col] = None    
        piece.row, piece.col = destRow, destCol
        self.grid[destRow][destCol] = piece
        self.turn = "black" if self.turn == "white" else "white"
        return True
    
class GameLogic:
    def __init__(self):
        self.board = BoardState()
        self.turn = "white"
    
    def legalMoves(self):
        legalMovesList = {}
        for i in range(8):
            for j in range(8):
                piece = self.board.grid[i][j]
                if piece is not None:
                    color = "W" if piece.color == "white" else "B"
                    key = piece.name + color
                    legalMovesList[key] = piece.get_moves(self.board)
        return legalMovesList