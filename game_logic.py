def inside(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7

class Piece:
    def __init__(self, color, name):
        self.name = name
        self.color = color
    
    def get_moves(self, board, row, col):
        return []

class SlidingPiece(Piece):
    def slide(self, board, row, col, directions):
        moves = []
        for xDir, yDir in directions:
            moveRow, moveCol = row + xDir, col + yDir
            while inside(moveRow, moveCol):
                target = board.grid[moveRow][moveCol]
                if target is None:
                    moves.append((moveRow, moveCol))
                else:
                    if target.color != self.color:
                        moves.append((moveRow, moveCol))
                    break
                moveRow += xDir
                moveCol += yDir
        return moves
    
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, "Pawn")
        
    def get_moves(self, board, row, col):
        moves = []
        side = -1 if self.color == "white" else 1
        start_row = 6 if self.color == "white" else 1

        if inside(row+side, col) and board.grid[row+side][col] is None: 
            moves.append((row+side,col))
            if row == start_row and board.grid[row+(2*side)][col] is None:
                    moves.append((row+(2*side),col))
                    
        for colDiff in (-1, 1):
            newRow, newCol = row + side, col + colDiff
            if inside(newRow, newCol):
                target = board.grid[newRow][newCol]
                if target and target.color != self.color:
                    moves.append((newRow, newCol))
        return moves
    
class Bishop(SlidingPiece):
    def __init__(self, color):
        super().__init__(color, "Bishop")

    def get_moves(self, board, row, col):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self.slide(board, row, col, directions)
    
class Rook(SlidingPiece):
    def __init__(self, color):
        super().__init__(color, "Rook")

    def get_moves(self, board, row, col):
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        return self.slide(board, row, col, directions)

class Queen(SlidingPiece):
    def __init__(self, color):
        super().__init__(color, "Queen")

    def get_moves(self, board, row, col):
        directions = [(-1, -1),(-1, 0),(-1, 1),(0, -1),(0, 1),(1, -1),(1, 0),(1, 1)]
        return self.slide(board, row, col, directions)

class King(Piece):
    def __init__(self, color):
        super().__init__(color, "King")

    def get_moves(self, board, row, col):
        moves = []
        directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, -1), (-1, 0), (0, -1), (1, -1)]
        
        for xDir, yDir in directions:
            moveRow = row + 1 * xDir
            moveCol = col + 1 * yDir
            if inside(moveRow, moveCol):
                target = board.grid[moveRow][moveCol]
                if target == None:
                    moves.append((moveRow, moveCol))
                else:
                    if target.color != self.color:
                        moves.append((moveRow, moveCol))
            else: return True
        return moves

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, "Knight")

    def get_moves(self, board, row, col):
        moves = []
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

        self.grid[0][0] = Rook("black")
        self.grid[0][7] = Rook("black")
        self.grid[7][0] = Rook("white")
        self.grid[7][7] = Rook("white")

        self.grid[0][2] = Bishop("black")
        self.grid[0][5] = Bishop("black")
        self.grid[7][2] = Bishop("white")
        self.grid[7][5] = Bishop("white")

        self.grid[0][3] = King("black")
        self.grid[7][3] = King("white")

        self.grid[0][4] = Queen("black")
        self.grid[7][4] = Queen("white")

        self.grid[0][3] = King("black")

        self.grid[0][1] = Knight("black")
        self.grid[0][6] = Knight("black")
        self.grid[7][1] = Knight("white")
        self.grid[7][6] = Knight("white")
                                
        for c in range(8):
            self.grid[1][c] = Pawn("black")
            self.grid[6][c] = Pawn("white")
    
    def move(self, row, col, destRow, destCol):
        piece = self.grid[row][col]
        
        if piece is None:
            return False
        if (destRow, destCol) not in piece.get_moves(self, row, col):
            return False
        #possibly add move class later
        self.grid[destRow][destCol] = piece
        self.grid[row][col] = None
        self.turn = "white" if self.turn == "black" else "black"
        return True
    
    def getPiece(self, row, col):
        return self.grid[row][col]