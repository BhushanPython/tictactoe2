"""
run a batch file on Google Cloud to generate all sequences for every depth from 1 to 24.  This will be run in a batch
on GCP instance.  This program will create a repository of XO sequences and store results in pickle dumps for use in
minimax
"""
from itertools import permutations
from pickle import dump
import re
from dataclasses import dataclass
import os
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

@dataclass
class GameSeq:
    seq: tuple  # sequence
    win_loss: str  # win loss from 'X' standpoint


def generate_permutes(depth: int) -> set[str]:
    """
    generates all strings for the given length of Xs and Os and pads with blanks so that the length is SIZE ** 2
    """
    assert depth <= SIZE ** 2
    o_count = depth // 2
    x_count: int = depth - o_count
    permutes = set(''.join(permute) + ' ' * (SIZE ** 2 - depth) for permute
                   in permutations(['X'] * x_count + ['O'] * o_count))
    return permutes


def check_win_loss_tie(cells: tuple) -> str | None:
    """
    rewritten win lose logic without using the class definitions
    """
    padded_cells = str(cells) + ' ' * ((SIZE ** 2) - len(cells))
    for pattern in WP:
        for mark in ['X', 'O']:
            try:
                if re.match(pattern.replace("?", mark), padded_cells):
                    return 'Win' if mark == 'X' else 'Loss'
            except AttributeError:
                print(f"Attribute error pattern is {pattern}, and type is {type(pattern)}")
    if padded_cells.count(' ') == 0:
        return 'Tie'
    return None


def build_up(depth: int) -> None:
    """
    builds up permutations of Xs and Os based on depth
    checks for tie/loss/win
    updates a holding structure
    pickle dumps into file
    """
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


def test_build_up():
    build_up(depth=3)
    return


def main():
    print("Starting the compute")
    for depth in range(1, SIZE ** 2):
        print(f"Building for depth {depth}")
        build_up(depth=depth)
    return



if __name__ == '__main__':
    main()
