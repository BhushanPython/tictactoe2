from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
import re
from functools import cached_property

# from tic_tac_toe.logic.validators import validate_grid
from tic_tac_toe.logic.exceptions import InvalidMove, InvalidWinningPattern
from tic_tac_toe.logic.params import SIZE, WINNING_LEN, WINNING_PATTERNS


class Mark(str, Enum):
    CROSS = "X"
    NAUGHT = "O"
    before_state: GameState
    after_state: GameState

    @property
    def other(self) -> Mark:
        if Mark.CROSS:
            return Mark.NAUGHT
        else:
            return Mark.CROSS


@dataclass(frozen=True)
class Move:
    mark: Mark
    place: int
    before_GameState: GameState
    after_GameState: GameState


@dataclass(frozen=True)
class Grid:
    size: int = SIZE  # number of rows and columns
    cells: str = " " * SIZE ** 2  # CFG change for flexible size of game
    winning_len: int = WINNING_LEN  # you could have a 5 by 5 with a winning length pf 4

    def __post_init__(self) -> None:
        if not re.match((r"^[\sXO]" + r"{" + str(self.size ** 2) + r"}$"), self.cells):
            raise ValueError(f"Must contain {self.size ** 2} cells containing: X, O, or space\n.",
                             f"Instead found this: {self.cells} of length {len(self.cells)}")

    def x_count(self) -> int:
        return self.cells.count("X")

    def y_count(self) -> int:
        return self.cells.count("O")

    def empty_count(self) -> int:
        return self.cells.count(" ")

    def winning_patterns(self) -> list[str]:
        try:
            return WINNING_PATTERNS[(SIZE, WINNING_LEN)]
        except KeyError:
            raise InvalidWinningPattern(f'Winning pattern not found for size {SIZE} and winning length {WINNING_LEN}')


@dataclass(frozen=True)
class GameState:
    grid: Grid
    starting_mark: Mark = Mark.CROSS

    @cached_property
    def current_mark(self) -> Mark:
        """
        whose turn is it "X" or "O ?
        """
        if self.grid.x_count() == self.grid.y_count():
            return self.starting_mark
        else:
            return self.starting_mark.other

    @cached_property
    def game_not_started(self) -> bool:
        return self.grid.empty_count() == self.grid.size ** 2

    @cached_property
    def game_over(self) -> bool:
        return self.winner or self.tie

    @cached_property
    def tie(self) -> bool:
        return self.grid.empty_count() == 0 and self.winner is None

    @cached_property
    def winner(self) -> str | None:
        for pattern in self.grid.winning_patterns():
            for mark in Mark:
                try:
                    if re.match(pattern.replace("?", mark), self.grid.cells):
                        return mark
                except AttributeError:
                    print(f"Attribute error pattern is {pattern}, and type is {type(pattern)}")
        return None

    @cached_property
    def winning_cells(self) -> list[int]:
        for pattern in self.grid.winning_patterns():
            for mark in Mark:
                try:
                    if re.match(pattern.replace("?", mark), self.grid.cells):
                        return [
                            match.start()
                            for match in re.finditer(r"\?", pattern)
                        ]
                except AttributeError:
                    print(f"Attribute error pattern is {pattern}, and type is {type(pattern)}")
        return []

    def make_move_to(self, place: int) -> Move:
        if place >= self.grid.size ** 2 or place < 0:
            raise InvalidMove('Index of place to move to is beyond range')
        if self.grid.cells[place] != ' ':
            raise InvalidMove('Attempt to mark a non empty cell.')
        return Move(
            mark=self.current_mark,
            place=place,
            before_GameState=self,
            after_GameState=GameState(
                Grid(size=SIZE, cells=self.grid.cells[:place] + self.current_mark + self.grid.cells[place + 1:],
                     winning_len=3),
                starting_mark=self.starting_mark
            )
        )

    @cached_property
    def possible_moves(self) -> list[Move]:
        moves = []
        if not self.game_over:
            for (pos, val) in enumerate(list(self.grid.cells)):
                if val == ' ':
                    moves.append(self.make_move_to(place=pos))
            return moves


def preview(gs: GameState):
    for i in range(gs.grid.size):
        print(gs.grid.cells[i * gs.grid.size: (i + 1) * gs.grid.size])
    return


def main():
    gs = GameState(grid=Grid(size=3, winning_len=3, cells='X O X O X'), starting_mark=Mark.CROSS)
    preview(gs)
    return


if __name__ == '__main__':
    main()
