import abc
import time
from random import randint, choice

from tic_tac_toe.logic.models import Grid, GameState, Mark, Move
from tic_tac_toe.logic.exceptions import InvalidMove
from abc import ABCMeta


class Player(metaclass=ABCMeta):
    def __init__(self, name: str, mark: Mark):
        self.name: str = "unchristened"
        self.mark = mark

    def make_move(self, game_state: GameState) -> GameState:
        if self.mark == game_state.current_mark:
            if move := self.get_move(game_state):
                return move.after_gamestate
            raise InvalidMove("Bad move or no more moves possible")
        else:
            raise InvalidMove(f"Its not player {self.name} 's turn")

    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Move | None:
        """implemented by the actual player classes"""


class ComputerPlayer(Player, metaclass=ABCMeta):
    def __init__(self, name: str, mark: Mark, delay_seconds: float = 0.25) -> None:
        super().__init__(name=name, mark=mark)
        self.delay_seconds = delay_seconds

    def get_move(self, game_state: GameState) -> Move | None:
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)

    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Move | None:
        """implement multiple computer players with their own move strategies """


class RandomComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        try:
            return choice(game_state.possible_moves)
        except IndexError:  # takes care of empty list - when no more moves are possible
            return None


class MiniMaxPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Move | None:
        return None


    def minimax(self, game_state: GameState) -> Move | None:
        possible_moves = game_state.possible_moves
        for move in possible_moves:
            if move.after_gamestate.winner in [self.mark, self.mark.other()]:
                # if winning or opponent winning in a move choose that
                return Move
            else:























