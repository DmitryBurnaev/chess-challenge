import pprint
import copy
import gc


class CanNotTakePositionException(Exception):
    pass


class Game(object):

    def __init__(self, dim_x, dim_y, figures_counts=None):
        self.boards = []
        self.uniq_boards_dict = {}
        self.dimension_x = dim_x
        self.dimension_y = dim_y
        # TODO: get figures from point of <Game obj> creation
        self.possible_figures = [King, Rock, Rock]

    def _create_combination(self, board):
        next_figure = board.next_figure()

        for cell in board.free_cells:
            new_board = self._new_board(board)
            try:
                new_board.place_figure(next_figure, cell[0], cell[1])
            except CanNotTakePositionException:
                del new_board
                # TODO: возможно нужно выяснить конфликты до того как создадим "лишнюю" доску
                continue

            if new_board.possible_figures:
                self._create_combination(new_board)
            else:
                new_board.is_ready = True
                board_hash = hash(new_board)
                if board_hash not in self.uniq_boards_dict:
                    self.uniq_boards_dict[board_hash] = new_board.serialize()
        del board
        gc.collect()

    def generate_combinations(self):
        board = self._new_board()
        self._create_combination(board)
        self._clear_uncompleted_boards()

    def _clear_uncompleted_boards(self):
        for board in filter(lambda x: not x.is_ready, reversed(self.boards)):
            index = self.boards.index(board)
            self.boards.pop(index)
        self.boards = list(set(self.boards))

    def _new_board(self, base_board=None):
        if not base_board:
            board = Board(self)
        else:
            board = copy.deepcopy(base_board)
        # self.boards.append(board)
        return board

    def render_results(self):
        print('<U>'.center(32, '-'))
        print(len(self.uniq_boards_dict.values()))
        # for board_figures in self.uniq_boards_dict.values():
        #     print(' | '.join(['<{type}> ({pos_x};{pos_y})'.format(**fig_dict) for fig_dict in board_figures]))
            # pprint.pprint(simple_board_dict)
        if not self.uniq_boards_dict:
            print('Sorry. Can not find combinations')
        print('-'.center(32, '-'))

    def run(self):
        self.generate_combinations()
        self.render_results()

    def test_attack_lines(self):
        board = Board(self)
        k = King(board, 1, 2)
        r = Rock(board, 1, 2)
        print('Rock attack')
        print(r.attack_lines())
        print('King attack')
        print(k.attack_lines())


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
        print('Create new board for needed figures: {}'.format(self.possible_figures))

    def __repr__(self):
        return '<Board> {}'.format(self._str_repr())

    def __str__(self):
        return '<Board> {}'.format(self._str_repr())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self._str_repr())

    def _str_repr(self):
        return ' | '.join(sorted([str(figure) for figure in self.figures]))

    def render(self):
        print(self._str_repr())

    def decrease_free_space(self, pos_x, pos_y):
        try:
            self.free_cells.remove([pos_x, pos_y])
        except ValueError:
            print('Can not decrease space [{}] for {}'.format([pos_x, pos_y], self.free_cells))

    def next_free_cell(self, current_cell):
        try:
            cur_index = self.free_cells.index(current_cell)
            return self.free_cells[cur_index + 1]
        except IndexError:
            return None

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


class FigureOnBoard(object):

    def __init__(self, board=None, pos_x=None, pos_y=None):
        self.board = board
        self.x, self.y = pos_x, pos_y
        self._take_position()

    def _take_position(self):
        if not self._can_take_position():
            raise CanNotTakePositionException

        self.board.decrease_free_space(self.x, self.y)
        for x, y in self.attack_lines():
            self.board.decrease_free_space(x, y)

    def _can_take_position(self):
        figure_positions = {(f.x, f.y) for f in self.board.figures}
        attack_cells = set(self.attack_lines())
        print(figure_positions, attack_cells)
        return not bool(figure_positions.intersection(attack_cells))

    def attack_lines(self):
        raise NotImplementedError

    def serialize(self):
        return {
            'type': self.__class__.__name__,
            'pos_x': self.x,
            'pos_y': self.y,
        }

    def __str__(self):
        return '{f.__class__.__name__} ({f.x};{f.y})'.format(f=self)


class King(FigureOnBoard):

    def attack_lines(self):
        return [(self.x - 1, self.y - 1),
                (self.x, self.y - 1),
                (self.x + 1, self.y - 1),
                (self.x + 1, self.y),
                (self.x + 1, self.y + 1),
                (self.x, self.y + 1),
                (self.x - 1, self.y + 1),
                (self.x - 1, self.y)]


class Rock(FigureOnBoard):
    def attack_lines(self):
        attack_cells = []
        for x in range(0, self.board.game.dimension_x):
            if (x, self.y) != (self.x, self.y):
                attack_cells.append((x, self.y))
        for y in range(0, self.board.game.dimension_y):
            if (self.x, y) != (self.x, self.y):
                attack_cells.append((self.x, y))
        return attack_cells


if __name__ == '__main__':
    game = Game(3, 3)
    # game.test_attack_lines()
    game.run()

