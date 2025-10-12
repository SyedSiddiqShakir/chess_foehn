
"""
Feed a PGN file in this and recieve a complete set of FEN states for the whole game.
The number of FEN states is equal to the number of half moves (not to be confused with a full move which is when 1 move is played by each player). 
"""
import chess
import mess_around as ma
import re

with open('chess_games_data\latestgame.pgn', 'r', encoding='utf-8') as myfile1:
    my_pgn = myfile1.read()

with open('chess_games_data\latestgame2.pgn', 'r', encoding='utf-8') as myfile2:
    my_pgn2 = myfile2.read()

pgn = open("chess_games_data\latestgame.pgn")
fg = chess.pgn.read_game(pgn)

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
    move = delimiter.join(moves)
    return move

def to_fen(pgn_string):
        pass

my_pgn = remove_headers(strip_lines(my_pgn))
my_pgn2 = remove_headers(strip_lines(my_pgn2))

cleaned_pgn = re.sub(r'\d+\.\s+', '', my_pgn).strip()
cleaned_pgn2 = re.sub(r'\d+\.\s+', '', my_pgn2).strip()

move_list = cleaned_pgn.split()
move_list2 = cleaned_pgn2.split()

del move_list2[-1]

print(move_list2)

board2 = chess.Board()
fen2 = board2.fen()
print(fen2)
print(move_list2[0])

board2_1 = board2.push_san(move_list2[0])
fen2_1 = board2.fen()
print(fen2_1)