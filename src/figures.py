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
        raise NotImplementedError

    def serialize(self):
        return {
            'type': self.__class__.__name__,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
        }

    def __str__(self):
        return '{f.__class__.__name__} ({f.pos_x};{f.pos_y})'.format(f=self)


class King(FigureOnBoard):

    def cells_to_attack(self):
        return [(self.pos_x - 1, self.pos_y - 1),
                (self.pos_x, self.pos_y - 1),
                (self.pos_x + 1, self.pos_y - 1),
                (self.pos_x + 1, self.pos_y),
                (self.pos_x + 1, self.pos_y + 1),
                (self.pos_x, self.pos_y + 1),
                (self.pos_x - 1, self.pos_y + 1),
                (self.pos_x - 1, self.pos_y)]


class Rock(FigureOnBoard):
    def cells_to_attack(self):
        attack_cells = []
        for x in range(0, self.board.game.dimension_x):
            if (x, self.pos_y) != (self.pos_x, self.pos_y):
                attack_cells.append((x, self.pos_y))
        for y in range(0, self.board.game.dimension_y):
            if (self.pos_x, y) != (self.pos_x, self.pos_y):
                attack_cells.append((self.pos_x, y))
        return attack_cells
