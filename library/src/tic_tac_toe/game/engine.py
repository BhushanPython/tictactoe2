from dataclasses import dataclass
from tic_tac_toe.game.players import Player, RandomComputerPlayer
from tic_tac_toe.game.renderers import Renderer, ConsoleRenderer
from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.models import GameState, Grid, Mark
from tic_tac_toe.logic.validators import validate_players
from typing import TypeAlias, Callable
from tic_tac_toe.logic.params import SIZE, WINNING_LEN

ErrorHandler: TypeAlias = Callable[[Exception], None]


@dataclass(frozen=True)
class TicTacToe:
    player1: Player
    player2: Player
    renderer: "Renderer"
    error_handler: ErrorHandler | None = None

    def __post_init__(self):
        validate_players(self.player1, self.player2)

    def play(self, starting_mark: Mark = Mark.CROSS) -> None:
        game_state = GameState(grid=Grid(size=SIZE, cells=Grid.cells, winning_len=WINNING_LEN),
                               starting_mark=starting_mark)
        # blank start
        while True:
            self.renderer.render(game_state)
            if game_state.game_over:
                break
            player = self.get_current_player(game_state)
            try:
                game_state = player.make_move(game_state)
            except InvalidMove as ex:
                if self.error_handler:
                    self.error_handler(ex)
                else:
                    raise InvalidMove('Invalid move attempted')

    # end of play 

    def get_current_player(self, game_state):
        if game_state.current_mark is self.player1.mark:
            return self.player1
        else:
            return self.player2


def test():
    player1 = RandomComputerPlayer(name="Random1", mark=Mark("X"))
    player2 = RandomComputerPlayer(name="Random2", mark=Mark("O"))
    t = TicTacToe(player1=player1, player2=player2, renderer=ConsoleRenderer, error_handler=None)
    t.play()
    return


def main():
    test()
    return

if __name__ == '__main__':
    main()






