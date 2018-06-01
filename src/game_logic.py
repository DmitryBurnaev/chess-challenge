import copy
import gc

from src.exceptions import CanNotTakePositionException
from src.figures import King, Rock

# Sorted by the number of attacked cells
ALIASES_FIGURES_MAP = (
    # ('queens', Rock),   # all lines under attack
    # ('bishops': Rock),  # diagonal lines under attack
    ('rooks', Rock),      # horizontal and vertical lines under attack
    ('kings', King),      # cells under attack only near the current position
    # ('knights': Rock   # special attacks
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
        # print('Create new board for needed figures: {}'.format(self.possible_figures))

    def __hash__(self):
        str_repr = ' | '.join(sorted([str(figure) for figure in self.figures]))
        return hash(str_repr)

    def decrease_free_space(self, pos_x, pos_y):
        try:
            self.free_cells.remove([pos_x, pos_y])
        except ValueError:
            pass
            # print('Can not decrease space [{}] for {}'.format([pos_x, pos_y], self.free_cells))

    def next_figure(self):
        try:
            return self.possible_figures.pop(0)
        except IndexError:
            return None

    def place_figure(self, figure_type, pos_x, pos_y):
        figure = figure_type(board=self, pos_x=pos_x, pos_y=pos_y)
        self.figures.append(figure)

    def serialize(self):
        return [figure.serialize() for figure in self.figures]
