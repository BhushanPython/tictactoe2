"""
This one time program builds the minimax point values for various positions and stores in file. In the players model
the minimax player simply reads the scores and determines the best move.
Scores are stored for two scenarios 1. grid, winning_len = 3,3 and 2. grid, winning_len = 5,4
"""
from itertools import permutations
import re
minmax_scores = {}
from tic_tac_toe.logic.models import Grid, GameState, Mark
from tic_tac_toe.logic.params import SIZE, WINNING_LEN, WINNING_PATTERNS
all_scores: dict = {}
hits: int = 0
misses: int = 0

WP = WINNING_PATTERNS[SIZE, WINNING_LEN]


def get_score(move, starting_mark: Mark, score: int) -> int:
    global all_scores, hits, misses
    new_game_state = move.after_gamestate
    if new_game_state.winner == starting_mark:
        all_scores[new_game_state.grid.cells] = 1
        score += 1
        misses += 1
    elif new_game_state.winner == starting_mark.other:
        all_scores[new_game_state.grid.cells] = -1
        score -= 1
        misses += 1
    elif new_game_state.tie is True:
        all_scores[new_game_state.grid.cells] = 0
        misses += 1
    else:
        for new_move in new_game_state.possible_moves:
            this_score = get_score(move=new_move, starting_mark=starting_mark, score=score)
            if this_score is not None:
                score += this_score
            all_scores[new_move.after_gamestate.grid.cells] = score
        all_scores[move.after_gamestate.grid.cells] = score
    all_scores[move.after_gamestate.grid.cells] = score
    return score




def test():
    global all_scores, hits, misses
    starting_point = cells = ''.join(['X', 'O', 'X', 'O', 'X', 'O', ' ', ' ', ' '])
    start_game_state = GameState(Grid(size=SIZE, winning_len=WINNING_LEN, cells=starting_point),
                                 starting_mark=Mark.CROSS)
    for move in start_game_state.possible_moves:
        score = get_score(move=move, starting_mark=Mark.CROSS, score=0)
        print(move, score)
    print('all scores follows...')
    print(all_scores)
    print(f'hits: {hits}, misses: {misses}')
    return





def test_winning_patterns():
    grid = Grid(size=SIZE, cells=' ' * (SIZE ** 2), winning_len=WINNING_LEN)
    print(grid.winning_patterns())


def check_win_loss_tie(cells: str, starting_mark=Mark.CROSS) -> str | None:
    """
    rewritten win lose logic without using the class definitions
    str must be SIZE ** 2 length
    """
    for pattern in WP:
        for mark in [Mark.CROSS, Mark.NAUGHT]:
            try:
                if re.match(pattern.replace("?", mark), cells):
                    return 'Win' if mark is starting_mark else 'Loss'
            except AttributeError:
                print(f"Attribute error pattern is {pattern}, and type is {type(pattern)}")
    if cells.count(' ') == 0:
        return 'Tie'
    return None


def test_winner():
    cells = '?....?....?....?.........'.replace('?.', 'XO')
    cells = cells.replace('.', ' ')
    grid = Grid(size=SIZE, cells=cells, winning_len=WINNING_LEN)
    game_state = GameState(grid=grid, starting_mark=Mark.CROSS)
    print(cells, game_state.winner)
    return


def test_check_win_loss_tie():
    depth = 20
    assert depth <= SIZE ** 2
    o_count = depth // 2
    x_count = depth - o_count
    permutes = [''.join(permute) + ' ' * (SIZE ** 2 - depth) for permute in permutations(['X'] * x_count + ['O'] * o_count)]
    for sequence in permutes:
        print(f'String is {sequence} and result is {check_win_loss_tie(sequence)}')
    return


def main():
    # test_winning_patterns() # succeeded
    # test_winner() # succeeded
    # test_generate_permutes() # succeeded
    # test_check_closed_permute()
    test_check_win_loss_tie()
    return


if __name__ == '__main__':
    main()
