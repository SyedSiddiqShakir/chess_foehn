
"""
Feed a PGN file in this and recieve a complete set of FEN states for the whole game.
The number of FEN states is equal to the number of half moves (not to be confused with a full move which is when 1 move is played by each player). 
"""
import chess
import src.data_exploration as ma
import re

pgn = open("chess_games_data\latestgame.pgn")
fg = chess.pgn.read_game(pgn)

#print(my_pgn2)
def strip_lines(content):
    lines = content.strip().split('\n')
    return lines

def remove_headers(lines):
    moves = []
    for line in lines:
        if not line.startswith('['):
            moves.append(line)
    moves = list(filter(None, moves))
    delimiter = ""
    move_string = delimiter.join(moves)
    return move_string

def convert_to_pgn_list(pgn_string):
        #convert to string if not done already and clean the pgn to only list objects
        pgn_string = remove_headers(strip_lines(str(pgn_string)))
        cleaned_pgn_string = re.sub(r'\d+\.\s+', '', pgn_string).strip()

        #divide all half moves into list objects
        pgn_list = cleaned_pgn_string.split()
        
        #deletes the game result (the last object always)
        del pgn_list[-1]
        return pgn_list

def pgn_to_fen(pgn_list: list):
    my_board = chess.Board()
    fen_list = []

    #iterate through the list
    for move in pgn_list:
        my_board.push_san(move)
        fen = my_board.fen()
        fen_list.append(fen)
    return fen_list


game = convert_to_pgn_list(fg)
print(game)

final_fen_list = pgn_to_fen(game)
print(final_fen_list)