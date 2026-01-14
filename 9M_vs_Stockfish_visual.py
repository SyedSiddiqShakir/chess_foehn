import sys
import os
import pygame
import chess
import chess.engine
import time

sys.path.append(os.getcwd())
from searchless_chess.src.engines import constants


STOCKFISH_PATH = r"S:\Everything German\Study Docs\SEM3\applications_of_ml\chess_Foehn\stockfish\stockfish-windows-x86-64-avx2.exe" 
STOCKFISH_DEPTH = 2

# Visual Settings
BOARD_SIZE = 640
SQUARE_SIZE = BOARD_SIZE // 8
FPS = 60
MOVE_DELAY = 0.5  # Seconds to wait between moves so we can see them

# Colors
WHITE_COLOR = (240, 217, 181)
BLACK_COLOR = (181, 136, 99)
HIGHLIGHT_COLOR = (100, 255, 100) # Green for last move
TEXT_COLOR_BLACK = (0, 0, 0)
TEXT_COLOR_WHITE = (255, 255, 255)

def draw_board(screen, board):
    """Draws the board and highlights the last move made."""
    for row in range(8):
        for col in range(8):
            # Draw Square
            color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

            # Highlight Last Move (Yellow/Green transparent)
            if board.move_stack:
                last_move = board.peek()
                # Check start square
                if (7 - chess.square_rank(last_move.from_square)) == row and chess.square_file(last_move.from_square) == col:
                     pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, 5)
                # Check end square
                if (7 - chess.square_rank(last_move.to_square)) == row and chess.square_file(last_move.to_square) == col:
                     pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, 5)

def draw_pieces(screen, board, font):
    """Draws the pieces."""
    piece_unicode = {
        'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
        'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
    }

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            symbol = piece_unicode[piece.symbol()]
            color = TEXT_COLOR_BLACK if piece.color == chess.BLACK else (250, 250, 250)
            text_surface = font.render(symbol, True, color)
            
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            text_rect = text_surface.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                                      row * SQUARE_SIZE + SQUARE_SIZE // 2))
            screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("9M (White) vs Stockfish (Black)")
    clock = pygame.time.Clock()

    font_name = pygame.font.match_font('segoeuisymbol') or pygame.font.match_font('arialunicodems')
    try:
        font = pygame.font.Font(font_name, int(SQUARE_SIZE * 0.9))
    except:
        font = pygame.font.SysFont(None, int(SQUARE_SIZE * 0.9))

    print("Loading 9M Engine...")
    try:
        engine_9m = constants.ENGINE_BUILDERS['9M']()
    except Exception as e:
        print(f"Error loading 9M: {e}")
        return

    print("Loading Stockfish...")
    try:
        stockfish = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    except Exception as e:
        print(f"Error loading Stockfish at {STOCKFISH_PATH}: {e}")
        print("Make sure stockfish.exe is in the folder!")
        return

    board = chess.Board()
    running = True
    game_over = False

    while running:
        # Handle Quit Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw Everything
        draw_board(screen, board)
        draw_pieces(screen, board, font)
        pygame.display.flip()

        # Check Game Over
        if board.is_game_over():
            if not game_over:
                print(f"Game Over! Result: {board.result()}")
                game_over = True
            continue 

        # Move Logic
        if not game_over:
            time.sleep(MOVE_DELAY)
            pygame.event.pump() 

            if board.turn == chess.WHITE:
                print("9M (White) is thinking...")
                try:
                    move = engine_9m.play(board)
                    board.push(move)
                    print(f"9M plays: {move.uci()}")
                except Exception as e:
                    print(f"9M Crashed: {e}")
                    running = False
            else:
                print("Stockfish (Black) is thinking...")
                try:
                    result = stockfish.play(board, chess.engine.Limit(STOCKFISH_DEPTH))
                    board.push(result.move)
                    print(f"Stockfish plays: {result.move.uci()}")
                except Exception as e:
                    print(f"Stockfish Crashed: {e}")
                    running = False

        clock.tick(FPS)

    # Cleanup
    stockfish.quit()
    pygame.quit()

if __name__ == '__main__':
    main()