"""
This file creates all winning patterns for a given grid size and winning length
This will be run one time and winning patterns created will be store using pickle dumps for use in the game project
"""
from __future__ import annotations
from itertools import permutations
from dataclasses import dataclass
from json import dump, dumps
from os import getcwd

DOT = '.'
MARKER = '?'


@dataclass
class Grid:
    size: int
    win_len: int

    def get_grid_string(self, grid_values) -> str:
        return ''.join([grid_values[(x, y)] for x in range(self.size) for y in range(self.size)])

    def get_empty_grid(self):
        grid_values: dict[tuple] = {}
        for (x, y) in [(x, y) for x in range(self.size) for y in range(self.size)]:
            grid_values[(x, y)] = DOT
        return grid_values

    def generate_win_vectors(self) -> list:
        """
        so how many lines can be there have the winning pattern for e.g. if size = 5, win_len = 4
        '????.', '.????' and '????'.  If found in a horizontal, vertical or diagonal they indicate a win
        where '?' is replaced by either 'X' or 'O'.
        Also note that multiple diagonals can hold winning patterns unlike in a 3 by 3 game
        """
        win_vectors: list = []
        for pad in range(0, self.size - self.win_len + 1):
            permute_string = MARKER + DOT * pad
            for x in permutations(permute_string):
                win_vector = list(''.join(x).replace(MARKER, MARKER * self.win_len))
                win_vectors.append(win_vector)
        return win_vectors

    def get_horizontal_position_vectors(self) -> map:
        return map(lambda y: [(i, y) for i in range(self.size)], range(self.size))

    def get_vertical_position_vectors(self) -> map:
        return map(lambda y: [(y, i) for i in range(self.size)], range(self.size))

    def get_nw_se_diagonal_position_vectors(self) -> map:
        return map(lambda diff: [(x, y) for x in range(self.size) for y in range(self.size)
                                 if y - x == diff],
                   range(-(self.size - self.win_len), self.size - self.win_len + 1))

    def get_ne_sw_diagonal_position_vectors(self) -> map:
        diff = self.size - self.win_len
        return map(lambda num: [(x, y) for x in range(self.size) for y in range(self.size)
                                if x + y == num], range(self.size - diff - 1, self.size + diff + 1))

    def get_winning_string(self, position_vector: list[tuple], win_vector: list[str]) -> str:
        """
        given a position vector will return a grid in string format that contains that winning pattern
        """
        grid_values = self.get_empty_grid()
        for ((x, y), val) in zip(position_vector, win_vector):
            grid_values[(x, y)] = val
        return ''.join(grid_values[(x, y)] for x in range(self.size) for y in range(self.size))

    def get_winning_patterns(self) -> list[str]:
        """
        creates a super set of all position vectors. then superimposes each winning vector on each position vector
        to generate all winning patterns
        """
        position_vectors: list = []
        winning_patterns: list[str] = []
        position_vectors += list(self.get_horizontal_position_vectors())
        position_vectors += list(self.get_vertical_position_vectors())
        position_vectors += list(self.get_ne_sw_diagonal_position_vectors())
        position_vectors += list(self.get_nw_se_diagonal_position_vectors())
        win_vectors = self.generate_win_vectors()

        for (p, w) in [(p, w) for p in position_vectors for w in win_vectors if len(p) == len(w)]:
            grid_values = self.get_empty_grid()
            for (x, y), val in zip(p, w):
                grid_values[(x, y)] = val
            winning_patterns.append(self.get_grid_string(grid_values=grid_values))
        return winning_patterns


if __name__ == '__main__':
    g = Grid(size=3, win_len=3)
    winning_patterns_33 = g.get_winning_patterns()

    g = Grid(size=5, win_len=4)
    winning_patterns_54 = g.get_winning_patterns()

    json_object_dict = {'all_patterns': [
                            {'length': '3', 'win_length': '3', 'winning_pattern': str(winning_patterns_33)},
                            {'length': '5', 'win_length': '4', 'winning_pattern': str(winning_patterns_54)}
                            ]
                        }

    json_object = dumps(json_object_dict)
    f_name = getcwd() + r'/winning_patterns.json'
    with open(f_name, 'w') as json_file:
        dump(json_object, json_file)
