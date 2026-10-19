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
        self.values = {"king" : 0, "queen": 8, "rook": 5, "bishop": 3, "knight": 3, "pawn": 1}
        super().__init__(depth)

    def choose_move(self, board):
        moves = board.get_all_legal_moves()
        if moves is None:
            return

        