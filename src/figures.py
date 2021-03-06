"""
This module provides figures logic and data descriptions.
You can extend the game logic by adding a new figure's type
(inherited from the class "FigureOnBoard")
"""


class FigureOnBoard(object):
    """ The base class for the description of the figures Logic
        used object's attributes:
            display_char - symbol for display on ASCI board
            board - current board
            pos_x, pos_y - current position on the board
    """

    display_char = None

    def __init__(self, board, pos_x, pos_y):
        self._cells_to_attack = []
        self.board = board
        self.pos_x, self.pos_y = pos_x, pos_y

    def can_take_position(self):
        """ Detect possibility for taking position: No one on the board is
            under the impact of this figure
        :return: True | False
        """

        figure_positions = {(f.pos_x, f.pos_y) for f in self.board.figures}
        attack_cells = set(self.cells_to_attack())
        return not bool(figure_positions.intersection(attack_cells))

    def cells_to_attack(self):
        """ Return cells for attack this figure on this board. This method
            gets correct attack cells and filters them

        :return: list of coordinates of cells to attack.
                 For example: [(0,1),(1,1)..]
        """
        if self._cells_to_attack:
            return self._cells_to_attack

        attack_cells = self._get_cells_to_attack()
        # removing self position
        while (self.pos_x, self.pos_y) in attack_cells:
            attack_cells.remove((self.pos_x, self.pos_y))

        # filtering cells outside of the board
        self._cells_to_attack = \
            list(filter(lambda x: x[0] >= 0 and x[1] >= 0, attack_cells))

        return self._cells_to_attack

    def _get_cells_to_attack(self):
        """ Every subclass must to override this method for getting correct
            cells to attack
        :return: list of coordinates of cells to attack.
        """
        raise NotImplementedError

    def serialize(self):
        """ Representing <FigureOnBoard> instance for storing important data
            to finally results

        :return: like dict-type object
        """
        return StoredFigure({
            'type': self.__class__.__name__,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'display_char': self.display_char
        })

    def __str__(self):
        return '{f.__class__.__name__} ({f.pos_x};{f.pos_y})'.format(f=self)


class StoredFigure(dict):
    """ Storage important data for every figure on the board.
        It helps to represent internal data with more shortly way.
    """
    def __str__(self):
        display_x = self['pos_x'] + 1
        display_y = self['pos_y'] + 1
        return '[{}] {} ({};{})'.format(self['display_char'], self['type'],
                                        display_x, display_y)


class King(FigureOnBoard):
    """ King figure on the board

           0 1 2 3
       0 | - * * *
       1 | - * K *
       2 | - * * *
    """
    display_char = 'K'

    def _get_cells_to_attack(self):
        return [(self.pos_x - 1, self.pos_y - 1),
                (self.pos_x, self.pos_y - 1),
                (self.pos_x + 1, self.pos_y - 1),
                (self.pos_x + 1, self.pos_y),
                (self.pos_x + 1, self.pos_y + 1),
                (self.pos_x, self.pos_y + 1),
                (self.pos_x - 1, self.pos_y + 1),
                (self.pos_x - 1, self.pos_y)]


class Rook(FigureOnBoard):
    """ Rook on the board

           0 1 2 3
       0 | - - * -
       1 | * * R *
       2 | - - * -
    """
    display_char = 'R'

    def _get_cells_to_attack(self):
        attack_cells = []
        # horizontal attack
        for coord_x in range(0, self.board.dimension_x):
            attack_cells.append((coord_x, self.pos_y))
        # vertical attack
        for coord_y in range(0, self.board.dimension_y):
            attack_cells.append((self.pos_x, coord_y))

        return attack_cells


class Queen(FigureOnBoard):
    """ Queen on the board

           0 1 2 3
       0 | - * * *
       1 | * * Q *
       2 | - * * *
    """
    display_char = 'Q'

    def _get_cells_to_attack(self):
        attack_cells = []
        board = self.board
        # horizontal attack
        for coord_x in range(0, board.dimension_x):
            attack_cells.append((coord_x, self.pos_y))
        # vertical attack
        for coord_y in range(0, board.dimension_y):
            attack_cells.append((self.pos_x, coord_y))

        # right and up
        coord_x, coord_y = self.pos_x, self.pos_y
        while coord_x < board.dimension_x and coord_y < board.dimension_y:
            attack_cells.append((coord_x, coord_y))
            coord_x += 1
            coord_y += 1

        # left and up
        coord_x, coord_y = self.pos_x, self.pos_y
        while coord_x >= 0 and coord_y < board.dimension_y:
            attack_cells.append((coord_x, coord_y))
            coord_x -= 1
            coord_y += 1

        # left and down
        coord_x, coord_y = self.pos_x, self.pos_y
        while coord_x >= 0 and coord_y >= 0:
            attack_cells.append((coord_x, coord_y))
            coord_x -= 1
            coord_y -= 1

        # right and down
        coord_x, coord_y = self.pos_x, self.pos_y
        while coord_x < board.dimension_x and coord_y >= 0:
            attack_cells.append((coord_x, coord_y))
            coord_x += 1
            coord_y -= 1

        return attack_cells


class Bishop(FigureOnBoard):
    """ Bishop on the board

           0 1 2 3
       0 | - * - *
       1 | - - B -
       2 | - * - *
    """

    display_char = 'B'

    def _get_cells_to_attack(self):
        attack_cells = []
        board = self.board

        # right and up
        coord_x, coord_y = self.pos_x, self.pos_y
        while coord_x < board.dimension_x and coord_y < board.dimension_y:
            attack_cells.append((coord_x, coord_y))
            coord_x += 1
            coord_y += 1

        # left and up
        coord_x, coord_y = self.pos_x, self.pos_y
        while coord_x >= 0 and coord_y < board.dimension_y:
            attack_cells.append((coord_x, coord_y))
            coord_x -= 1
            coord_y += 1

        # left and down
        coord_x, coord_y = self.pos_x, self.pos_y
        while coord_x >= 0 and coord_y >= 0:
            attack_cells.append((coord_x, coord_y))
            coord_x -= 1
            coord_y -= 1

        # right and down
        coord_x, coord_y = self.pos_x, self.pos_y
        while coord_x < board.dimension_x and coord_y >= 0:
            attack_cells.append((coord_x, coord_y))
            coord_x += 1
            coord_y -= 1

        return attack_cells


class Knight(FigureOnBoard):
    """ Knight on the board

           0 1 2 3
       0 | * - - -
       1 | - - N -
       2 | * - - -
    """

    display_char = 'N'

    def _get_cells_to_attack(self):
        attack_cells = [(self.pos_x - 1, self.pos_y - 2),
                        (self.pos_x + 1, self.pos_y - 2),
                        (self.pos_x - 2, self.pos_y - 1),
                        (self.pos_x - 2, self.pos_y + 1),
                        (self.pos_x - 1, self.pos_y + 2),
                        (self.pos_x + 1, self.pos_y + 2),
                        (self.pos_x + 2, self.pos_y + 1),
                        (self.pos_x + 2, self.pos_y - 1)]
        return attack_cells
