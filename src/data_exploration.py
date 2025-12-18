import chess
import chess.pgn

with open('chess_games_data\latestgame.pgn', 'r', encoding='utf-8') as myfile1:
    content1 = myfile1.read()
with open('chess_games_data\latestgame2.pgn', 'r', encoding='utf-8') as myfile2:
    content2 = myfile2.read()
with open('chess_games_data\latestgame3.pgn', 'r', encoding='utf-8') as myfile3:
    content3 = myfile3.read()

pgn = open("chess_games_data\lichess_elite_2013-09.pgn")
fg = chess.pgn.read_game(pgn)
#print(fg)


if __name__ == '__main__':
    pass