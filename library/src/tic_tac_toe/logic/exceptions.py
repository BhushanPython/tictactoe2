class InvalidWinningPattern(Exception):
    """ will be raised if winning patterns for the size and winning length is not available"""
class InvalidGameState(Exception):
    """Raised when invalid game state found."""


class InvalidMove(Exception):
    """Raised when invalid move received found."""


class InvalidPlayer(Exception):
    """Raised when invalid player setup found."""
