import copy
import gc

from src.exceptions import CanNotTakePositionException
from src.figures import King, Rook, Queen, Bishop, Knight


# Sorted by the number of attacked cells
ALIASES_FIGURES_MAP = (
    ('queens', Queen),  # all lines under attack
    ('bishops', Bishop),  # diagonal lines under attack
    ('rooks', Rook),  # horizontal and vertical lines under attack
    ('kings', King),  # cells under attack only near the current position
    ('knights', Knight)   # special attacks
)


class Game(object):

    def __init__(self, dim_x, dim_y, figures_numbers):
        self.serialized_boards = {}
        self.dimension_x = dim_x
        self.dimension_y = dim_y
        self.possible_figures = []
        self.figures_numbers = figures_numbers

        for alias, figure_type in ALIASES_FIGURES_MAP:
            figures_count = figures_numbers.get(alias, 0)
            self.possible_figures.extend([figure_type] * figures_count)

        self.render_initial_data()

    def _create_combinations(self, board):
        next_figure = board.next_figure()

        for cell in board.free_cells:
            new_board = copy.deepcopy(board)
            try:
                new_board.place_figure(next_figure, cell[0], cell[1])
            except CanNotTakePositionException:
                del new_board
                continue

            if new_board.possible_figures:
                self._create_combinations(new_board)
            else:
                board_hash = hash(new_board)
                self.serialized_boards.setdefault(board_hash,
                                                  new_board.serialize())
        del board
        gc.collect()

    def generate_combinations(self):
        board = Board(self)
        self._create_combinations(board)

    def render_boards(self):
        print('Result'.center(40, '-'))
        if self.serialized_boards:
            print('Found {} combinations:'.format(len(self.serialized_boards)))
            for combinations in self.serialized_boards.values():
                print(' | '.join(map(str, combinations)))
                self.render_graphic_board(combinations)
                print('-'.center(20, '-'))
        else:
            print('Sorry, no matches were found for your query.')
        print('-'.center(40, '-'))

    def render_initial_data(self):
        print('Initial configuration'.center(40, '-'))
        print('Boards dimensions: {} x {}'.format(self.dimension_x,
                                                  self.dimension_y))
        print('Figures set:')
        for alias, numbers in self.figures_numbers.items():
            if numbers > 0:
                print('{:^10}:{:^5}'.format(alias.capitalize(), numbers))

    def render_graphic_board(self, combinations):
        cells = {(cell['pos_x'], cell['pos_y']): cell for cell in combinations}
        res = '    '
        for x in range(self.dimension_x):
            res += '{} '.format(x+1)
        print(res)
        for y in range(self.dimension_y):
            res = '{} | '.format(y+1)
            for x in range(self.dimension_x):
                if (x, y) in cells:
                    res += cells[(x, y)]['display_char'] + ' '
                else:
                    res += '- '
            print(res)

    def run(self):
        self.generate_combinations()
        self.render_boards()


class Board(object):
    is_ready = False

    def __init__(self, game):
        self.game = game
        self.figures = []
        self.free_cells = []
        self.possible_figures = game.possible_figures

        for x in range(self.game.dimension_x):
            for y in range(self.game.dimension_y):
                self.free_cells.append([x, y])

    def __hash__(self):
        str_repr = ' | '.join(sorted([str(figure) for figure in self.figures]))
        return hash(str_repr)

    def decrease_free_space(self, pos_x, pos_y):
        try:
            self.free_cells.remove([pos_x, pos_y])
        except ValueError:
            pass

    def next_figure(self):
        if not self.possible_figures:
            return None
        return self.possible_figures.pop(0)

    def place_figure(self, figure_type, pos_x, pos_y):
        figure = figure_type(board=self, pos_x=pos_x, pos_y=pos_y)
        self.figures.append(figure)

    def serialize(self):
        return [figure.serialize() for figure in self.figures]
