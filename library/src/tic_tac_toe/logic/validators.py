from __future__ import annotations
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING is True:
    from tic_tac_toe.logic.models import Grid, GameState, Mark
    from tic_tac_toe.game.players import Player
from tic_tac_toe.logic.exceptions import InvalidGameState, InvalidPlayer


def validate_grid(grid: Grid) -> None:
    if not re.match(r"^[\sXO]{9}$", grid.cells):
        raise ValueError("Must contain 9 cells of: X, O, or space")
    return


def validate_game_state(game_state: GameState) -> None:
    validate_number_of_marks(game_state.grid)
    validate_starting_mark(game_state.grid, game_state.starting_mark)
    validate_winner(game_state.grid, game_state.starting_mark, game_state.winner)
    return


def validate_number_of_marks(grid: Grid):
    if grid.x_count() < grid.y_count():
        raise InvalidGameState('More Os than Xs. Game state in error.')
    elif abs(grid.x_count() - grid.empty_count()) > 1:
        raise InvalidGameState('Difference between number of Xs and Os must not be more than 1.  Game state in error.')
    return


def validate_starting_mark(grid: Grid, starting_mark: Mark) -> None:
    if grid.x_count() > grid.y_count() and starting_mark != Mark.CROSS:
        raise InvalidGameState('More Xs than Os but starting mark is O. Game state in error.')
    if grid.x_count() > grid.y_count() and starting_mark != Mark.NAUGHT:
        raise InvalidGameState('More Os than Xs but starting mark is O. Game state in error.')
    return


def validate_winner(grid: Grid, starting_mark: Mark, winner: str) -> None:
    if starting_mark == Mark.NAUGHT:
        if winner == Mark.NAUGHT:
            if grid.y_count() <= grid.x_count():
                raise InvalidGameState('Starting Mark, Winner and Counts of X and Os don\'t reconcile.')
        elif winner == Mark.CROSS:
            if grid.x_count() != grid.y_count():
                raise InvalidGameState('Starting Mark, Winner and Counts of X and Os don\'t reconcile.')
    elif starting_mark == Mark.CROSS:
        if winner == Mark.CROSS:
            if grid.x_count() <= grid.y_count():
                raise InvalidGameState('Starting Mark, Winner and Counts of X and Os don\'t reconcile.')
        elif winner == Mark.NAUGHT:
            if grid.x_count() != grid.y_count():
                raise InvalidGameState('Starting Mark, Winner and Counts of X and Os don\'t reconcile.')
    return


def validate_players(player1: Player, player2: Player) -> None:
    if player1.name.strip() == '':
        raise InvalidPlayer('Player 1 name not provided')
    if player2.name.strip() == '':
        raise InvalidPlayer('Player 2 name not provided')
    if player1.mark in ['X', 'O'] and player1.mark in ['X', 'O'] \
            and player1.mark is not player2.mark:
        pass
    else:
        raise InvalidPlayer('Invalid setup of players')
    return


