import game_logic
from ai import MinMaxAI
import argparse

parser = argparse.ArgumentParser(prog="Chess")
parser.add_argument("--headless", action="store_true")
args = parser.parse_args()

def run_headless():
    board = game_logic.BoardState()

    white_ai = MinMaxAI(depth=1)
    black_ai = MinMaxAI(depth=1)

    move_count = 0
    while True:
        if board.turn == "white":
          ai = white_ai
        else:
          ai = black_ai
        move = ai.choose_move(board)
        if move is None:
            if board.in_check(board.turn):
              print(f"Game over, {board.turn} won")
              break
            else:
              print("stalemate")
              break
        start_row, start_col, end_row, end_col = move
        print(f"Turn {move_count}, {board.turn}, ({start_row}, {start_col}) -> ({end_row}, {end_col})")
        board.simulate_move(start_row, start_col, end_row, end_col)
        move_count += 1
        if move_count > 500:
          break


def run_gui():
  import renderer
  renderer.main_loop(MinMaxAI(depth=10))
                 

if (args.headless):
  run_headless()
else:
  run_gui()