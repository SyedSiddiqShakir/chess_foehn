import chess

with open('chess_games_data\latestgame.pgn', 'r', encoding='utf-8') as myfile1:
    content1 = myfile1.read()
with open('chess_games_data\latestgame2.pgn', 'r', encoding='utf-8') as myfile2:
    content2 = myfile2.read()
with open('chess_games_data\latestgame3.pgn', 'r', encoding='utf-8') as myfile3:
    content3 = myfile3.read()

def strip_lines(content):
    lines = content.strip().split('\n')
    return lines

def remove_headers(lines):
    moves = []
    for line in lines:
        if not line.startswith('['):
            moves.append(line)
    moves = list(filter(None, moves))
    return moves

print(remove_headers(strip_lines(content1)))