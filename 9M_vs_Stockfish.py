import sys
import os
import time
import chess
import chess.engine
import datetime

sys.path.append(os.getcwd())
from searchless_chess.src.engines import constants

from config_pars import load_config

#config file
config = load_config()
STOCKFISH_PATH = config.get("STOCKFISH_PATH", "stochfish.exe") 
STOCKFISH_DEPTH = 2 

def play_match():
    print("Loading DeepMind 9M Engine...")
    try:
        engine_9m = constants.ENGINE_BUILDERS['9M']()
        print("DeepMind 9M Loaded")
    except Exception as e:
        print(f"Error loading 9M: {e}")
        return

    print(f"Loading Stockfish from: {STOCKFISH_PATH}")
    if not os.path.exists(STOCKFISH_PATH):
        print(f"Error: Could not find '{STOCKFISH_PATH}'.")
        print("Please download Stockfish and put the .exe in this folder.")
        return

    try:
        stockfish = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        print("Stockfish Loaded")
    except Exception as e:
        print(f"Error loading Stockfish: {e}")
        return

    board = chess.Board()
    
    # User choice: Who plays White?
    print("\nWho plays White?")
    print("[1] DeepMind 9M")
    print("[2] Stockfish")
    choice = input("Enter 1 or 2: ").strip()
    
    white_player = "9M" if choice == "1" else "Stockfish"
    black_player = "Stockfish" if choice == "1" else "9M"
    
    print(f"\nSTARTING MATCH: {white_player} (White) vs {black_player} (Black)\n")
    time.sleep(1)

    # Game Loop
    while not board.is_game_over():
        print(f"\nMove {board.fullmove_number} | {white_player if board.turn == chess.WHITE else black_player} to move")
        print(board)
        
        # Determine current player
        current_player = white_player if board.turn == chess.WHITE else black_player

        if current_player == "9M":
            print(">> 9M is thinking...")
            start = time.time()
            best_move = engine_9m.play(board)
            end = time.time()
            print(f"   9M plays: {best_move.uci()} ({end-start:.2f}s)")
            board.push(best_move)

        else:
            print(">> Stockfish is thinking...")
            result = stockfish.play(board, chess.engine.Limit(depth=STOCKFISH_DEPTH))
            print(f"   Stockfish plays: {result.move.uci()}")
            board.push(result.move)

    # Game Over
    print("GAME OVER")
    print(f"Result: {board.result()}")
    print(f"Winner: {board.outcome().winner}")
    
    # Print PGN for analysis
    print("\nFinal PGN:")
    game = chess.pgn.Game.from_board(board)
    game.headers["White"] = white_player
    game.headers["Black"] = black_player
    print(game)

    #save as file with unique name
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_result = board.result().replace("/", "-") # Fixes "1/2-1/2" for filenames
    
    filename = f"9m_vs_stockfish_{safe_result}_{board.fullmove_number}mv_{timestamp}.pgn"
    
    with open(filename, "w", encoding="utf-8") as pgn_file:
        print(game, file=pgn_file, end="\n\n")
    
    print(f"Saved PGN file to '{filename}'")

    # Cleanup
    stockfish.quit()

if __name__ == "__main__":
    play_match()