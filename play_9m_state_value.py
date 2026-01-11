#systems
import sys
import os
import chess # type: ignore
sys.path.append(os.getcwd())

#locals
from searchless_chess.src.engines import constants
from searchless_chess.src import transformer
from searchless_chess.src import tokenizer
from searchless_chess.src import utils

"""
#globals (removed because we used engines/constants.py)
import chess
import jax
import jax.numpy as jnp
import orbax.checkpoint
from flax.training import orbax_utils
"""

def play_game():
    ai_engine = constants.ENGINE_BUILDERS['9M']()
    board = chess.Board()

    while not board.is_game_over():
        print(f"\n{board}")

        #human move
        if board.turn == chess.WHITE:
            while True:
                move_str = input("Human move".strip())
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    board.push(move)
                    break
                else:
                    print(f"{move_str} is an illegal move or invalid format")
        else:
            #ai move
            print("model is thinking")
            best_move = ai_engine.play(board) #main guy
            print(f"model moves {best_move}")
            board.push(best_move)
    print(board.result())

    if __name__ == '__main__':
        play_game()