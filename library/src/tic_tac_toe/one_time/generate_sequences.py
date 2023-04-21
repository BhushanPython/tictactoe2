"""
run a batch file on Google Cloud to generate all sequences for every depth from 1 to 24.  This will be run in a batch
on GCP instance.  This program will create a repository of XO sequences and store results in pickle dumps for use in
minimax
"""
from more_itertools import distinct_permutations
from itertools import permutations
from itertools import chain
from collections import namedtuple
from pickle import dump, load
import re
from dataclasses import dataclass
import os
from tic_tac_toe.logic.models import Mark
from typing import Iterator
SIZE = 5
WP = [
    "?....?....?....?.........", ".....?....?....?....?....", ".?....?....?....?........",
    "......?....?....?....?...", "..?....?....?....?.......", ".......?....?....?....?..",
    "...?....?....?....?......", "........?....?....?....?.", "....?....?....?....?.....",
    ".........?....?....?....?", "????.....................", ".????....................",
    ".....????................", "......????...............", "..........????...........",
    "...........????..........", "...............????......", "................????.....",
    "....................????.", ".....................????", "...?...?...?...?.........",
    "....?...?...?...?........", "........?...?...?...?....", ".........?...?...?...?...",
    ".....?.....?.....?.....?.", "?.....?.....?.....?......", "......?.....?.....?.....?",
    ".?.....?.....?.....?....."
]
DB_HOME = './DB'
WIN = 1
LOSS = 2
TIE = 0


move = namedtuple('move', 'Mark, place, score')
win_loss: str = ''
place: int | None
score: int | None
best_move: move | None
seq_data = namedtuple('seq_data', 'win_loss, moves, best_move')
seq_db = {tuple: seq_data}
win_loss_db: dict[tuple: int] = {}


def generate_permutes(depth: int) -> Iterator:
    """
    generates all strings for a given number of Xs and Os - depth which are of length size ** 2
    and checks for win. Returns a namedtuple
    """
    o_depth = depth // 2
    x_depth = depth - o_depth
    permutes = distinct_permutations('X' * x_depth + 'O' * o_depth + ' ' * (SIZE ** 2 - x_depth - o_depth))
    return permutes


def check_win_loss_tie(permute: tuple) -> int | None:
    """
    rewritten win lose logic without using the class definitions
    expects tuples of length SIZE ** 2
    Win/loss from 'X' point of view
    """
    try:
        win_loss_tie = win_loss_db[permute]
        return win_loss_tie
    except KeyError:
        result = None
        cells = ''.join(permute)
        for pattern in WP:
            for mark in ['X', 'O']:
                try:
                    if re.match(pattern.replace("?", mark), cells):
                        result = WIN if mark == 'X' else LOSS
                except AttributeError:
                    print(f"Attribute error, pattern is {pattern}, and type is {type(pattern)}")
        if cells.count(' ') == 0:
            result = TIE
        win_loss_db[permute] = result
        return result


def build_win_loss_db():
    permutes = ()
    for depth in range(10, 11):
        permutes_new = generate_permutes(depth=depth)
        temp_permutes = permutes
        permutes = chain(temp_permutes, permutes_new)
    for permute in permutes:
        win_or_loss = check_win_loss_tie(permute)
        seq_db[permute] = seq_data(win_loss=win_or_loss, moves=None, best_move=None)
    with open('win_loss_data.dict', 'wb') as sequence_db:
        dump(seq_db, sequence_db)
    return
    # end of function


"""
def build_up(depth: int) -> None:
    builds up permutations of Xs and Os based on depth
    checks for tie/loss/win
    updates a holding structure
    pickle dumps into file

    assert depth < SIZE ** 2
    gs_db_1 = []
    gs_db_2 = []
    starting_string = 'X' * depth + 'O' * (depth - 1)
    permutes = set(permutations(starting_string))
    for permute in permutes:
        gs = GameSeq(seq=tuple(permute), win_loss=check_win_loss_tie(cells=permute))
        gs_db_1.append(gs)
    print(f'For X depth {depth} and O depth {depth -1} {len(gs_db_1)} sequences found')
    starting_string = 'X' * depth + 'O' * depth
    permutes = set(permutations(starting_string))
    for permute in permutes:
        gs = GameSeq(seq=tuple(permute), win_loss=check_win_loss_tie(cells=permute))
        gs_db_2.append(gs)
    print(f'For X depth {depth} and O depth {depth} {len(gs_db_2)} sequences found')
    gs_db = gs_db_1 + gs_db_2
    f_name = DB_HOME + '/seq_db_' + 'X_' + str(depth) + '_O_' + str(depth)
    with open(f_name, 'wb') as db:
        dump(gs_db, db)
    print(f'Written to file d{f_name} with details {os.stat(f_name)}')
    print('Process over')
    return
"""


def fast_list_gen():
    """
    trying to look at alternatives for faster creation of sequences required for minimax
    """
    perms = permutations('X' * 7 + 'Y' * 7)
    last = None
    uniques = set()
    count = 0
    unique_count = 0
    while True:
        try:
            new = next(perms)
            count += 1
            if new != last:
                uniques.add(new)
                unique_count += 1
                last = new
            if count % 1000000 == 0:
                print(f'count = {count} and uniques is {unique_count}')
        except StopIteration:
            return
    # end of function


def test_read_gcp_data():
    """
    read files from gcp processed data and check validity and performance
    """
    with open(r'/Users/bhushan/coding/tictactoe2/library/src/tic_tac_toe/one_time/seq_db_X_6_O_6', 'rb') \
            as seq_database:
        seq_db_data = load(seq_database)
    print(f'length 6 by 6 data is {len(seq_db_data)}')
    for row in seq_db_data:
        seq = row.seq
        result = check_win_loss_tie(seq)
        if result is not None:
            print(seq, result)
    return


def test_build_up():
    build_win_loss_db()
    return


def main():
    # print("Starting the compute")
    # for depth in range(1, SIZE ** 2):
    #     print(f"Building for depth {depth}")
    #     build_up(depth=depth)
    # test_read_gcp_data()
    # fast_list_gen()
    test_build_up()
    return


if __name__ == '__main__':
    main()
