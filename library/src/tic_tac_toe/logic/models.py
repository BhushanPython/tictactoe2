from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
import re
from functools import cached_property

# from tic_tac_toe.logic.validators import validate_grid

WINNING_PATTERNS = (    # CFG
    "???......",
    "...???...",
    "......???",
    "?..?..?..",
    ".?..?..?.",
    "..?..?..?",
    "?...?...?",
    "..?.?.?..",
)


class Mark(str, Enum):
    CROSS = "X"
    NAUGHT = "O"
    before_state: GameState
    after_state: GameState

    @property
    def other(self) -> Mark:
        return Mark.CROSS if Mark.NAUGHT else Mark.NAUGHT


@dataclass(frozen=True)
class Grid:
    size: int = 3  # number of rows and columns
    cells: str = " " * size**2  # CFG change for flexible size of game
    winning_len: int = 3  # you could have a 5 by 5 with a winning length pf 4

    def __post_init__(self) -> None:
        validate_grid(self)

    def x_count(self) -> int:
        return self.cells.count("X")

    def y_count(self) -> int:
        return self.cells.count("O")

    def empty_count(self) -> int:
        return self.cells.count(" ")

    def winning_patterns(self) -> list[str]:
        return ['']



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
        return self.grid.empty_count() == 9  # CFG change for flexible size of game

    @cached_property
    def game_over(self) -> bool:
        return False

    @cached_property
    def tie(self) -> bool:
        return self.grid.empty_count == 0 and self.winner is None

    @cached_property
    def winner(self) -> str | None:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return mark
        return None

    @cached_property
    def winning_cells(self) -> list[int]:
        for pattern in WINNING_PATTERNS:
            for mark in Mark:
                if re.match(pattern.replace("?", mark), self.grid.cells):
                    return [
                        match.start()
                        for match in re.finditer(r"\?", pattern)
                    ]
        return []

