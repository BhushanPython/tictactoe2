from tic_tac_toe.game.engine import TicTacToe
from tic_tac_toe.game.players import RandomComputerPlayer
from tic_tac_toe.logic.models import Mark
from tic_tac_toe.game.renderers import ConsoleRenderer

player1 = RandomComputerPlayer(name="Random1", mark=Mark("X"))
player2 = RandomComputerPlayer(name="Random2", mark=Mark("O"))

TicTacToe(player1=player1, player2=player2, renderer=ConsoleRenderer()).play()