import sys
import os
import chess #type: ignore 
import chess.engine #type: ignore
import chess.pgn #type: ignore
import pandas as pd #type: ignore
import time
import datetime
import random
sys.path.append(os.getcwd())
from searchless_chess.src.engines import constants
from config_pars import load_config

# CONFIGURATION
config = load_config()
STOCKFISH_PATH = config.get("STOCKFISH_PATH", "stockfish.exe")

# EXPERIMENT SETTINGS
MODEL_NAME = '270M'  # Options: '9M', '136M', '270M'
GAMES_PER_DEPTH = 1 
DEPTHS_TO_TEST = [1, 2] # depth levels, can simply add or remove

# Filer
OUTPUT_FOLDER = "benchmark_data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
SUMMARY_CSV = os.path.join(OUTPUT_FOLDER, f"summary_{MODEL_NAME}_vs_SF_1to{max(DEPTHS_TO_TEST)}_{GAMES_PER_DEPTH}_gamesperdepth.csv")
DETAILED_CSV = os.path.join(OUTPUT_FOLDER, f"detailed_{MODEL_NAME}_vs_SF__1to{max(DEPTHS_TO_TEST)}_{GAMES_PER_DEPTH}_gamesperdepth.csv")
PGN_FILENAME = os.path.join(OUTPUT_FOLDER, f"benchmark_{MODEL_NAME}_vs_SF_1to{max(DEPTHS_TO_TEST)}_{GAMES_PER_DEPTH}_gamesperdepth.pgn")

def play_one_game(model, stockfish, stockfish_depth, model_color):
    board = chess.Board()
    game_start_time = time.time()
    
    # Metadata for PGN
    game = chess.pgn.Game()
    game.headers["Event"] = f"Benchmark {MODEL_NAME} vs SF_d{stockfish_depth}"
    game.headers["White"] = f"{MODEL_NAME}" if model_color == chess.WHITE else f"Stockfish_d{stockfish_depth}"
    game.headers["Black"] = f"Stockfish_d{stockfish_depth}" if model_color == chess.WHITE else f"{MODEL_NAME}"
    game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")
    
    node = game 

    crash_loss = False
    
    while not board.is_game_over():
        # Play Move
        if board.turn == model_color:
            try:
                move = model.play(board)
            except:
                print("Model crash/illegal move.")
                crash_loss = True
                break
        else:
            try:
                res = stockfish.play(board, chess.engine.Limit(depth=stockfish_depth))
                move = res.move
            except:
                print("Stockfish crash.")
                break # Should rarely happen

        board.push(move)
        node = node.add_variation(move)

    # Game Over Processing
    game_duration = time.time() - game_start_time
    result = board.result()
    game.headers["Result"] = result
    
    # Save PGN
    with open(PGN_FILENAME, "a", encoding="utf-8") as f:
        print(game, file=f, end="\n\n")

    outcome = board.outcome()
    
    # Calculate Points (from Model Perspective)
    score = 0.0
    winner_str = "Draw"
    
    if crash_loss:
        score = 0.0
        winner_str = "Stockfish (Crash)"
    elif outcome.winner == model_color:
        score = 1.0
        winner_str = MODEL_NAME
    elif outcome.winner is None:
        score = 0.5
        winner_str = "Draw"
    else:
        score = 0.0
        winner_str = "Stockfish"

    # Return rich stats dictionary
    return {
        "score": score,
        "moves": board.fullmove_number,
        "time_sec": game_duration,
        "winner": winner_str,
        "termination": str(outcome.termination).split('.')[-1] if outcome else "CRASH",
        "fen": board.fen()
    }

def run_benchmark():
    print(f"BENCHMARK: {MODEL_NAME} vs STOCKFISH")
    print(f"Saving to: {OUTPUT_FOLDER}")
    
    # Load Engines
    try:
        model_engine = constants.ENGINE_BUILDERS[MODEL_NAME]()
        stockfish = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        print("Engines Loaded.")
    except Exception as e:
        print(f"Error loading engines: {e}")
        return

    summary_data = []
    detailed_data = []

    for depth in DEPTHS_TO_TEST:
        print(f"\n{MODEL_NAME} vs SF Depth {depth} ({GAMES_PER_DEPTH} games)")
        
        # Depth Stats Accumulators
        wins, losses, draws = 0, 0, 0
        white_wins, black_wins = 0, 0
        total_moves = 0
        total_time = 0

        for i in range(GAMES_PER_DEPTH):
            model_color = chess.WHITE if i % 2 == 0 else chess.BLACK
            color_label = "White" if model_color == chess.WHITE else "Black"
            
            print(f" Game {i+1} ({MODEL_NAME} as {color_label}): ", end="", flush=True)
            
            # PLAY GAME
            stats = play_one_game(model_engine, stockfish, depth, model_color)
            
            # Update Depth Stats
            if stats["score"] == 1.0: 
                wins += 1
                if model_color == chess.WHITE: white_wins += 1
                else: black_wins += 1
                print("WIN")
            elif stats["score"] == 0.5: 
                draws += 1
                print("DRAW")
            else: 
                losses += 1
                print("LOSS")
            
            total_moves += stats["moves"]
            total_time += stats["time_sec"]

            # Save DETAILED (Per-Game) Row
            detailed_data.append({
                "Model": MODEL_NAME,
                "Opponent_Depth": depth,
                "Game_Number": i+1,
                "Model_Color": color_label,
                "Score": stats["score"],
                "Winner": stats["winner"],
                "Moves": stats["moves"],
                "Time_Sec": round(stats["time_sec"], 2),
                "Termination": stats["termination"]
            })
            # Save Detailed CSV immediately
            pd.DataFrame(detailed_data).to_csv(DETAILED_CSV, index=False)

        # Calculate Averages for Summary
        win_rate = ((wins + (draws * 0.5)) / GAMES_PER_DEPTH) * 100
        avg_moves = total_moves / GAMES_PER_DEPTH
        avg_time = total_time / GAMES_PER_DEPTH

        print(f" > Result: {win_rate:.1f}% | Avg Moves: {avg_moves:.1f}")

        # Save SUMMARY (Per-Depth) Row
        summary_data.append({
            "Depth": depth,
            "Total_Games": GAMES_PER_DEPTH,
            "Win_Rate_%": win_rate,
            "Wins": wins,
            "Losses": losses,
            "Draws": draws,
            "White_Wins": white_wins,
            "Black_Wins": black_wins,
            "Avg_Moves": round(avg_moves, 1),
            "Avg_Time_Sec": round(avg_time, 1)
        })
        pd.DataFrame(summary_data).to_csv(SUMMARY_CSV, index=False)

    print("\nBenchmark Complete!")
    stockfish.quit()

if __name__ == "__main__":
    run_benchmark()