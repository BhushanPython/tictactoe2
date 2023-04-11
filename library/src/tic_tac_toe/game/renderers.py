import abc
from typing import Iterable
from tic_tac_toe.logic.models import GameState


class Renderer:
    @abc.abstractmethod
    def render(self, game_state: GameState) -> None:
        """implement your own renderer"""


class ConsoleRenderer(Renderer):
    def render(self, game_state: GameState) -> None:
        clear_screen()
        if game_state.winner:
            print_blinking(game_state.grid.cells, game_state.winning_cells)
            print(f"{game_state.winner} wins \N{party popper}")
        else:
            print_solid(game_state.grid.cells)
            if game_state.tie:
                print("No one wins this time \N{neutral face}")


# following functions are outside the class definition
def clear_screen():
    print("\033c", end="")


def blink(text: str) -> str:
    return f"\033[5m{text}\033[0m"


def print_blinking(cells: Iterable[str], positions: Iterable[int]) -> None:
    mutable_cells = list(cells)
    for position in positions:
        mutable_cells[position] = blink(mutable_cells[position])
    print_solid(mutable_cells)


def print_solid(cells: Iterable[str]) -> None:
    length = len(list(cells))  # just to get rid of a warning from PyCharm when using len(cells) directly
    size = int(length ** 0.5)
    left_gutter: int = 6  # reasonable even number
    row_header = ' ' * left_gutter + ' | '. join([chr(i) for i in range(ord('A'), ord('Z') + 1)][:size])
    print(row_header)
    row_separator = ' ' * int(left_gutter/2) + '_' * (len(row_header) - int(left_gutter/2))
    for i in range(size):
        print(row_separator)
        # row = ' ' * (int(left_gutter/2) - len(str(i)) - 1) + str(i) + ' ' \
        #       + '|' + ' ' * (int(left_gutter/2) - len(str(i))) + \
        #       ' | '.join([x for x in cells[i * size: (i + 1) * size]])

        row = ' ' * (int(left_gutter/2) - len(str(i)) - 1) + str(i)  \
              + '|' + ' ' * (int(left_gutter/2) - len(str(i))) + \
              ' | '.join([x for x in cells[i * size: (i + 1) * size]])
        print(row)
    print('\n')
    return


def test():
    print_solid(['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'X', 'X', 'O', 'X', 'O', 'X', 'O', 'X',
                 'X', 'X', 'X', 'O', 'X', 'O', 'X', 'O', 'X'])


def main():
    test()


if __name__ == '__main__':
    main()
