import game_logic
import random


class AI:
    def __init__(self, depth=1):
        self.depth = depth

    def choose_move(self, board):
        moves = board.get_all_legal_moves()
        if not moves:
            return

        roster = random.choice(moves)
        start_pos = roster[0]
        end_pos = random.choice(roster[1])

        return start_pos[0], start_pos[1], end_pos[0], end_pos[1]

class MinMaxAI(AI):
    def __init__(self, depth=2):
        self.values = {"King" : 0, "Queen": 8, "Rook": 5, "Bishop": 3, "Knight": 3, "Pawn": 1}
        super().__init__(depth)
    def get_moves(self, board):
        moves = []
        for start, dests in board.get_all_legal_moves():
            for end in dests:
                moves.append((start[0], start[1], end[0], end[1]))

        return moves
   
    def evalute(self, board):
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board.getPiece(row, col)
                if piece:
                    if piece.color == "white":
                        score += self.values[piece.name]
                    else:
                        score -= self.values[piece.name]
        return score
    def minimax(self, board, depth):
        if depth == 0:
            return self.evalute(board)
        moves = self.get_moves(board)
        if not moves:
            return self.evalute(board)
        if board.turn == "white":
            best_score = float("-inf")
            for move in moves:
                r1, c1, r2, c2 = move
                board.simulate_move(r1,c1,r2,c2)
                score = self.minimax(board, depth - 1)
                board.undo_move()
                best_score = max(best_score, score)
        else:
            best_score = float("inf")
            for move in moves:
                r1, c1, r2, c2 = move
                board.simulate_move(r1,c1,r2,c2)
                score = self.minimax(board, depth - 1)
                board.undo_move()
                best_score = min(best_score, score)
        return best_score
    def choose_move(self, board):
        moves = self.get_moves(board)
        if moves is None:
            return
        best_move = None
        if board.turn == "white":
            best_score = float("-inf")
            for move in moves:
                r1, c1, r2, c2 = move
                board.simulate_move(r1,c1,r2,c2)
                score = self.minimax(board, self.depth - 1)
                board.undo_move()
                if score > best_score:
                    best_score = score
                    best_move = move
        else:
            best_score = float("inf")
            for move in moves:
                r1, c1, r2, c2 = move
                board.simulate_move(r1,c1,r2,c2)
                score = self.minimax(board, 1)
                board.undo_move()
                if score < best_score:
                    best_score = score
                    best_move = move
        return best_move