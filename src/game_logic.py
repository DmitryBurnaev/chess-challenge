""" Module for implementation the game logic.
It is using for run-mode (basic usages) and test-mode (check of the game logic)

"""
import copy
import gc
import concurrent.futures
import os

from src.exceptions import GameArgumentsValidationError
from src.figures import King, Rook, Queen, Bishop, Knight
from src.logger import get_logger, get_log_file_handler

# Sorted by the number of attacked cells
ALIASES_FIGURES_MAP = (
    ('queens', Queen),    # all lines under attack
    ('bishops', Bishop),  # diagonal lines under attack
    ('rooks', Rook),      # horizontal and vertical lines under attack
    ('kings', King),      # cells under attack only near the current position
    ('knights', Knight)   # special attacks
)


class Game(object):
    """ The main class for creating possible chess combinations """
    logger = get_logger()

    def __init__(self, dim_x, dim_y, figures_numbers, result_to_file=False):
        self.serialized_boards = []
        self._result_boards_dict = {}  # uses for tmp storing uniq boards comb.
        self.dimension_x = dim_x
        self.dimension_y = dim_y
        self.possible_figures = []
        self.figures_numbers = figures_numbers
        self._validate_params()

        for alias, figure_type in ALIASES_FIGURES_MAP:
            # initial list of possible figure's types.Such as: [KING, QUEEN,..]
            figures_count = figures_numbers.get(alias, 0)
            self.possible_figures.extend([figure_type] * figures_count)

        if result_to_file:
            file_handler = get_log_file_handler()
            self.logger.addHandler(file_handler)

    def _validate_params(self):
        """ This method helps to check incoming params for combinations """

        dimensions = self.dimension_x * self.dimension_y
        if dimensions <= 0:
            raise GameArgumentsValidationError(
                'Dimensions must be greater then 0'
            )
        assert isinstance(self.figures_numbers, dict)

        if dimensions <= sum(self.figures_numbers.values()):
            raise GameArgumentsValidationError(
                'Dimensions must be greater then total number of figures'
            )

    def _create_combinations(self, board):
        """ Recursive logic for calculating combinations """

        next_figure_class = board.next_figure()

        for pos_x, pos_y in board.free_cells:
            # step over free cells for trying to place figure on this board
            new_figure = next_figure_class(board, pos_x, pos_y)
            if not new_figure.can_take_position():
                del new_figure
                continue

            new_board = copy.deepcopy(board)
            new_board.place_figure(next_figure_class, pos_x, pos_y)

            if new_board.possible_figures:
                self._create_combinations(new_board)
            else:
                board_hash = hash(new_board)
                self._result_boards_dict.setdefault(
                    board_hash, new_board.serialize()
                )
        del board
        gc.collect()
        return self._result_boards_dict

    def generate_combinations(self):
        """ It runs logic to generate all combinations.
            Founded combinations will store to self.serialized_boards.
        """
        if not self.possible_figures:
            return
        # get next figure
        next_figure = self.possible_figures.pop(0)
        start_board = Board(self)
        st_boards = []
        for pos_x, pos_y in start_board.free_cells:
            board = copy.deepcopy(start_board)
            board.place_figure(next_figure, pos_x, pos_y)
            st_boards.append(board)

        if os.getenv('TEST_MODE'):
            # running generation in single process (for correct coverage)
            for _board in st_boards:
                self._create_combinations(_board)
        else:
            # using process pull for running the program in main case
            with concurrent.futures.ProcessPoolExecutor() as executor:
                for res in executor.map(self._create_combinations, st_boards):
                    self._result_boards_dict.update(res)

        del start_board
        gc.collect()
        self.serialized_boards = self._result_boards_dict.values()

    def render_boards(self):
        """ Display result of work this application. """

        self.logger.info('Result'.center(40, '-'))
        if self.serialized_boards:
            self.logger.info(
                'Found {} combinations:'.format(len(self.serialized_boards))
            )
            for combinations in self.serialized_boards:
                self.logger.info(' | '.join(map(str, combinations)))
                self._render_graphic_board(combinations)
                self.logger.info('-'.center(20, '-'))
        else:
            self.logger.info('Sorry, no matches were found for your query.')
        self.logger.info('-'.center(40, '-'))

    def render_initial_data(self):
        """ Display data received to generate combinations """

        self.logger.info('Initial configuration'.center(40, '-'))
        self.logger.info('Boards dimensions: {} x {}'.format(self.dimension_x,
                                                  self.dimension_y))
        self.logger.info('Figures set:')
        for alias, numbers in self.figures_numbers.items():
            if numbers > 0:
                self.logger.info(
                    '{:^12}:{:^5}'.format(alias.capitalize(), numbers)
                )

    def _render_graphic_board(self, combinations):
        """ Render ASCI board with generated combination """

        cells = {(cell['pos_x'], cell['pos_y']): cell for cell in combinations}
        res = '    '
        for coord_x in range(self.dimension_x):
            res += '{} '.format(coord_x+1)
        self.logger.info(res)
        for coord_y in range(self.dimension_y):
            res = '{} | '.format(coord_y+1)
            for coord_x in range(self.dimension_x):
                if (coord_x, coord_y) in cells:
                    res += cells[(coord_x, coord_y)]['display_char'] + ' '
                else:
                    res += '- '
            self.logger.info(res)

    def run(self):
        """ Run generation of all possible combinations and display them to
            the screen
        """
        self.render_initial_data()
        self.generate_combinations()
        self.render_boards()


class Board(object):
    """ Class for storing temporary data to generate combinations in recursive
        mode
    """

    def __init__(self, game):
        self.dimension_x = game.dimension_x
        self.dimension_y = game.dimension_y
        self.possible_figures = game.possible_figures
        self.figures = []
        self.free_cells = []

        for coord_x in range(self.dimension_x):
            for coord_y in range(self.dimension_y):
                self.free_cells.append([coord_x, coord_y])

    def __hash__(self):
        """ Used to provide uniq for board's combination"""

        str_repr = ' | '.join(sorted([str(figure) for figure in self.figures]))
        return hash(str_repr)

    def decrease_free_space(self, pos_x, pos_y):
        """ Removing free cells after placing a new figure to the board """

        try:
            self.free_cells.remove([pos_x, pos_y])
        except ValueError:
            pass

    def next_figure(self):
        """ Getting next of possible figure's class for this board

        :return: subclass of <FigureOnBoard>
        """

        if not self.possible_figures:
            return None
        return self.possible_figures.pop(0)

    def place_figure(self, figure_class, pos_x, pos_y):
        """ Take position for specified figure

        :param figure_class: class for generate instance
                             (subclass for FigureOnBoard)
        :param pos_x: coordinate X for figure on this board
        :param pos_y: coordinate Y for figure on this board
        """
        figure = figure_class(board=self, pos_x=pos_x, pos_y=pos_y)
        self.figures.append(figure)
        self.decrease_free_space(figure.pos_x, figure.pos_y)
        for coord_x, coord_y in figure.cells_to_attack():
            self.decrease_free_space(coord_x, coord_y)

    def serialize(self):
        """ Represent all important data for storing to result collection"""

        return [figure.serialize() for figure in self.figures]
