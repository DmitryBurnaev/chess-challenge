from src.exceptions import CanNotTakePositionException


class FigureOnBoard(object):

    def __init__(self, board=None, pos_x=None, pos_y=None):
        self.board = board
        self.pos_x, self.pos_y = pos_x, pos_y
        self._take_position()

    def _take_position(self):
        # TODO: may be we have to realize this logic for <Board instance>..
        if not self._can_take_position():
            raise CanNotTakePositionException

        self.board.decrease_free_space(self.pos_x, self.pos_y)
        for x, y in self.cells_to_attack():
            self.board.decrease_free_space(x, y)

    def _can_take_position(self):
        figure_positions = {(f.pos_x, f.pos_y) for f in self.board.figures}
        attack_cells = set(self.cells_to_attack())
        return not bool(figure_positions.intersection(attack_cells))

    def cells_to_attack(self):
        attack_cells = self._get_cells_to_attack()
        # remove self position
        while (self.pos_x, self.pos_y) in attack_cells:
            attack_cells.remove((self.pos_x, self.pos_y))
        return filter(lambda x: x[0] >= 0 and x[1] >= 0, attack_cells)

    def _get_cells_to_attack(self):
        raise NotImplementedError

    def serialize(self):
        return StoredFigure({
            'type': self.__class__.__name__,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
        })

    def __str__(self):
        return '{f.__class__.__name__} ({f.pos_x};{f.pos_y})'.format(f=self)


class StoredFigure(dict):
    def __str__(self):
        display_x = self['pos_x'] + 1
        display_y = self['pos_y'] + 1
        return '{} ({};{})'.format(self['type'], display_x, display_y)


class King(FigureOnBoard):

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
    def _get_cells_to_attack(self):
        attack_cells = []
        # horizontal attack
        for x in range(0, self.board.game.dimension_x):
            attack_cells.append((x, self.pos_y))
        # vertical attack
        for y in range(0, self.board.game.dimension_y):
            attack_cells.append((self.pos_x, y))

        return attack_cells


class Queen(FigureOnBoard):
    def _get_cells_to_attack(self):
        attack_cells = []
        board = self.board
        # horizontal attack
        for x in range(0, board.game.dimension_x):
            attack_cells.append((x, self.pos_y))
        # vertical attack
        for y in range(0, board.game.dimension_y):
            attack_cells.append((self.pos_x, y))
        # right and up
        x, y = self.pos_x, self.pos_y
        while x < board.game.dimension_x and y < board.game.dimension_y:
            attack_cells.append((x, y))
            x += 1
            y += 1
        # left and up
        x, y = self.pos_x, self.pos_y
        while x >= 0 and y < board.game.dimension_y:
            attack_cells.append((x, y))
            x -= 1
            y += 1
        # left and down
        x, y = self.pos_x, self.pos_y
        while x >= 0 and y >= 0:
            attack_cells.append((x, y))
            x -= 1
            y -= 1
        # right and down
        x, y = self.pos_x, self.pos_y
        while x < board.game.dimension_x and y >= 0:
            attack_cells.append((x, y))
            x += 1
            y -= 1

        return attack_cells


class Bishop(FigureOnBoard):
    def _get_cells_to_attack(self):
        attack_cells = []
        board = self.board
        # right and up
        x, y = self.pos_x, self.pos_y
        while x < board.game.dimension_x and y < board.game.dimension_y:
            attack_cells.append((x, y))
            x += 1
            y += 1
        # left and up
        x, y = self.pos_x, self.pos_y
        while x >= 0 and y < board.game.dimension_y:
            attack_cells.append((x, y))
            x -= 1
            y += 1
        # left and down
        x, y = self.pos_x, self.pos_y
        while x >= 0 and y >= 0:
            attack_cells.append((x, y))
            x -= 1
            y -= 1
        # right and down
        x, y = self.pos_x, self.pos_y
        while x < board.game.dimension_x and y >= 0:
            attack_cells.append((x, y))
            x += 1
            y -= 1

        return attack_cells


class Knight(FigureOnBoard):
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
