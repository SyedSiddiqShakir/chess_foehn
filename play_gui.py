"""
    A GUI to play against the models, maybe a modular GUI later :)
"""
import sys
print("I am running from:", sys.executable)
import os
import pygame #type: ignore
import chess #type: ignore
sys.path.append(os.getcwd())
from searchless_chess.src.engines import constants

#configs
BOARD_SIZE = 640 #pixels
SQUARE_SIZE = BOARD_SIZE // 8

#colors
WHITE_COLOR = (149, 141, 141)
BLACK_COLOR = (128, 42, 43)
HIGHLIGHT_COLOR = (255,33,140)
TEXT_COLOR_WHITE = (255, 255, 255)
TEXT_COLOR_BLACK = (0,0,0)
FPS = 60

#functions
def draw_board(screen, board, selected_square=None):
    """Draws the board squares and highlights"""
    #square
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                color = WHITE_COLOR
            else:
                color = BLACK_COLOR

            #draw 
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

            #highlight square
            if selected_square is not None:
                sel_row, sel_col = 7 - chess.square_rank(selected_square), chess.square_file(selected_square)
                if sel_row == row and sel_col == col:
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, 4)

def draw_pieces(screen, board, font):
    """Draws the pieces"""
    #mapping
    piece_unicode = {
        'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
        'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
    }

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            symbol = piece_unicode[piece.symbol()]

            #calc
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)

            #text color
            if piece.color == chess.BLACK:
                color = TEXT_COLOR_BLACK
            else:
                color = (50, 50, 50)
            
            if piece.color == chess.WHITE:
                color = (250, 250, 250)
            
            #show (render)
            text_surface = font.render(symbol, True, color)
            text_rect = text_surface.get_rect(center=(col*SQUARE_SIZE + SQUARE_SIZE // 2,
                                                      row*SQUARE_SIZE + SQUARE_SIZE // 2))
            screen.blit(text_surface, text_rect)

    
def get_square_under_mouse(pos):
    """Hover definitions"""
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return chess.square(col, 7 - row)

def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption("Chess against 9M searchless model")
    clock = pygame.time.Clock()

    try:    
        font = pygame.font.SysFont("segoeuisymbol", int(SQUARE_SIZE*0.9))
    except:
        font = pygame.font.SysFont(None, int(SQUARE_SIZE*0.9))

    #load model
    ai_engine = constants.ENGINE_BUILDERS['9M']()
    board = chess.Board()
    selected_square = None
    running = True

    while running:
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if board.turn == chess.WHITE and not board.is_game_over():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_square = get_square_under_mouse(event.pos)
                    if selected_square is None:
                        piece = board.piece_at(clicked_square)
                        if piece and piece.color == chess.WHITE:
                            selected_square = clicked_square
                    else:
                        move = chess.Move(selected_square, clicked_square)

                        if move.promotion is None and board.piece_at(selected_square).piece_type == chess.PAWN:
                            if chess.square_rank(clicked_square) in [0, 7]:
                                move.promotion = chess.QUEEN

                        if move in board.legal_moves:
                            board.push(move)
                            selected_square = None #remove selection after move
                        else:
                            piece = board.piece_at(clicked_square)
                            if piece and piece.color == chess.WHITE:
                                selected_square = clicked_square
                            else:
                                selected_square = None
        
        #draw
        draw_board(screen, board, selected_square)
        draw_pieces(screen, board, font)

        #model moves
        if board.turn == chess.BLACK and not board.is_game_over():
            pygame.display.flip() #maybe deactivate this idk

            print("Model thinking")
            try:
                best_move = ai_engine.play(board)
                board.push(best_move)
                print(f"Model played {best_move}")
            except Exception as e:
                print(f"{e}")
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()           




if __name__ == '__main__':
    main()