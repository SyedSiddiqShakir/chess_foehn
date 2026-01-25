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
MODEL_NAME = '9M'  # Options: '9M', '136M', '270M'
GAMES_PER_DEPTH = 2 # Total games per depth level
DEPTHS_TO_TEST = [1, 2, 3] # The difficulty stairs, [1, 2, 3, 4, 5, 6, 7, 8, 10, 12]

# Filer
OUTPUT_FOLDER = "benchmark_data"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
CSV_FILENAME = os.path.join(OUTPUT_FOLDER, f"benchmark_results_{MODEL_NAME}_vs_stockfish_1to{max(DEPTHS_TO_TEST)}_{GAMES_PER_DEPTH}_gamesperdepth.csv")
PGN_FILENAME = os.path.join(OUTPUT_FOLDER, f"benchmark_games_{MODEL_NAME}_vs_stockfish_1to{max(DEPTHS_TO_TEST)}_{GAMES_PER_DEPTH}_gamesperdepth.pgn")

def play_one_game(model, stockfish, stockfish_depth, model_color):
    board = chess.Board()
    
    # Metadata for PGN
    game = chess.pgn.Game()
    game.headers["Event"] = f"Benchmark {MODEL_NAME} vs SF_d{stockfish_depth}"
    game.headers["White"] = f"{MODEL_NAME}" if model_color == chess.WHITE else f"Stockfish_d{stockfish_depth}"
    game.headers["Black"] = f"Stockfish_d{stockfish_depth}" if model_color == chess.WHITE else f"{MODEL_NAME}"
    game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")
    
    node = game # For PGN recording

    while not board.is_game_over():
        # Play Move
        if board.turn == model_color:
            try:
                move = model.play(board)
            except:
                print("Model crashed/illegal move. Resigning.")
                return 0 # Loss due to crash
        else:
            try:
                # Stockfish move limited by DEPTH
                res = stockfish.play(board, chess.engine.Limit(depth=stockfish_depth))
                move = res.move
            except:
                return 1 # Win (opponent crash)

        board.push(move)
        node = node.add_variation(move) # Add to PGN

    # Determine Result from Model's perspective
    # 1 = Win, 0 = Loss, 0.5 = Draw
    result = board.result()
    game.headers["Result"] = result
    
    # Save this single game to PGN immediately (so we don't lose data if crash)
    with open(PGN_FILENAME, "a", encoding="utf-8") as f:
        print(game, file=f, end="\n\n")

    outcome = board.outcome()
    if outcome.winner == model_color:
        return 1.0
    elif outcome.winner is None:
        return 0.5
    else:
        return 0.0

def run_benchmark():
    print(f"STARTING BENCHMARK: {MODEL_NAME} vs STOCKFISH")
    print(f"Depths: {DEPTHS_TO_TEST}")
    print(f"Games per depth: {GAMES_PER_DEPTH}")
    
    # Load Model
    print(f"Loading {MODEL_NAME} Model (This may take a minute)...")
    try:
        model_engine = constants.ENGINE_BUILDERS[MODEL_NAME]()
        print(f"Model {MODEL_NAME} Loaded.")
    except Exception as e:
        print(f"Failed to load {MODEL_NAME}. Check checkpoint folder name.")
        print(f"Error: {e}")
        return

    # Load Stockfish
    try:
        stockfish = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        print("Stockfish Loaded.")
    except Exception as e:
        print(f"Stockfish not found at {STOCKFISH_PATH}")
        return

    results_data = []

    # Main Loop
    for depth in DEPTHS_TO_TEST:
        print(f"\n--- {MODEL_NAME} vs Stockfish at Depth {depth} ---")
        wins, losses, draws = 0, 0, 0
        start_time = time.time()

        for i in range(GAMES_PER_DEPTH):
            # Alternate colors: Even games = Model White, Odd games = Model Black
            model_color = chess.WHITE if i % 2 == 0 else chess.BLACK
            color_name = "White" if model_color == chess.WHITE else "Black"
            
            print(f"  Game {i+1}/{GAMES_PER_DEPTH} (Model is {color_name})...", end="", flush=True)
            
            score = play_one_game(model_engine, stockfish, depth, model_color)
            
            if score == 1.0: 
                wins += 1
                print(" WIN")
            elif score == 0.5: 
                draws += 1
                print(" DRAW")
            else: 
                losses += 1
                print(" LOSS")

        # Calculate Stats for this depth
        total_score = wins + (draws * 0.5)
        win_rate = (total_score / GAMES_PER_DEPTH) * 100
        duration = (time.time() - start_time) / 60

        print(f"  > Depth {depth} Result: W:{wins} D:{draws} L:{losses} | Win Rate: {win_rate:.1f}% | Time: {duration:.1f}m")

        # Store Data
        results_data.append({
            "Depth": depth,
            "Games": GAMES_PER_DEPTH,
            "Wins": wins,
            "Draws": draws,
            "Losses": losses,
            "Win_Rate_Pct": win_rate,
            "Raw_Score": total_score
        })

        # Save CSV intermediate (backup)
        df = pd.DataFrame(results_data)
        df.to_csv(CSV_FILENAME, index=False)

    print("\nBenchmark Complete!")
    print(f"Data saved to {CSV_FILENAME} for {MODEL_NAME} vs Stockfish Depths {DEPTHS_TO_TEST} with {GAMES_PER_DEPTH} games per depth")
    print(f"PGNs saved to {PGN_FILENAME} for {MODEL_NAME} vs Stockfish Depths {DEPTHS_TO_TEST} with {GAMES_PER_DEPTH} games per depth")
    stockfish.quit()

if __name__ == "__main__":
    run_benchmark()