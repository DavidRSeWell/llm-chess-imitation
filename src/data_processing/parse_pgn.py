import argparse
import os
import logging
import json
import chess
import chess.pgn as pgn
import bz2
import glob

from os import path
from collections import OrderedDict
from contextlib import suppress

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s: %(message)s")


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--source_file", type=str, help="PGN dir")
    parser.add_argument("--output_dir", type=str, help="Output directory")
    parser.add_argument("--max_games", default=10_000_000, type=int, help="Max games to parse")

    parsed_args = parser.parse_args()
    assert (path.exists(parsed_args.source_file))
    if not path.exists(parsed_args.output_dir):
        os.makedirs(parsed_args.output_dir)

    return parsed_args


def parse_pgn(source_file: str, output_dir: str, max_games: int = 1000):
    basename = path.splitext(path.basename(source_file))[0]
    output_file = path.join(output_dir, f"{basename}_uci.txt")

    game_counter = 0
    error_counter = 0
    with open(output_file, 'w') as output_f, open(source_file) as source_f:
        current_header = None
        while True:
            try:
                game = pgn.read_game(source_f)
                headers = game.headers
                board = game.board()
                if game is None:
                    break
                white_player = headers["White"].replace("(wh)", "").strip()
                black_player = headers["Black"].replace("(bl)", "").strip()
                if len(white_player) > 1:
                    current_header = ["".join(white_player.split(",")).replace(" ","_"), "".join(black_player.split(",")).replace(" ","_"), headers["Result"]]
                #if len(white_player) <= 1 or len(black_player) <= 1:
                #    continue

                player_list = [white_player, black_player]
                move_list = []
                for move in game.mainline_moves():
                    move_list.append(board.uci(move))
                    board.push(move)


                if len(move_list) > 0:
                    move_list = current_header[:2] + move_list + [current_header[2]]
                #    move_list = move_list + [headers["Result"]]
                #else:
                #    continue
                if len(move_list) <= 10:
                    continue
                
                output_f.write(" ".join(move_list) + "\n")

                game_counter += 1
                if game_counter % 1e4 == 0:
                    logger.info(f"{game_counter} games processed")

                if game_counter >= max_games:
                    break
            except (ValueError, UnicodeDecodeError) as e:
                error_counter += 1
                pass

    logger.info(f"Extracted {game_counter} games at {output_file} failed to extract {error_counter}")


if __name__ == '__main__':
    source_file = "/Users/davidsewell/Data/Chess/millionbase-2.5.pgn"
    output_dir = "/Users/davidsewell/Data/Chess/"
    max_games = 1000
    parse_pgn(source_file=source_file, output_dir=output_dir, max_games=max_games)
