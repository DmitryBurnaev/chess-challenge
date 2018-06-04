""" Providing exceptions for correct work of the game logic
"""


class CanNotTakePositionException(Exception):
    """ Exception for detecting trying to place figure to invalid cell """
    pass


class GameArgumentsValidationError(Exception):
    """ Exception for detecting creation game with invalid arguments """
    pass
