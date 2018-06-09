import io
import logging
import os
import sys
import unittest
from contextlib import contextmanager

from src.exceptions import GameArgumentsValidationError
from src.figures import Queen, King, Rook
from src.game_logic import Board, Game


class GameInitialTestCase(unittest.TestCase):
    """ Testing logic for initial the game instance """

    def test_board_size(self):
        board = Board(Game(3, 4, {}))
        self.assertEqual(len(board.free_cells), 12)

        board = Board(Game(1, 8, {}))
        self.assertEqual(len(board.free_cells), 8)

    def test_possibility_figures(self):
        k_count, r_count, q_count = 3, 2, 4
        game = Game(3, 4, {'kings': k_count, 'rooks': r_count,
                           'queens': q_count})
        self.assertEqual(len(game.possible_figures),
                         sum([k_count, r_count, q_count]))
        self.assertEqual(game.possible_figures.count(King), k_count)
        self.assertEqual(game.possible_figures.count(Rook), r_count)
        self.assertEqual(game.possible_figures.count(Queen), q_count)

    def test_fail_for_fake_combinations(self):
        with self.assertRaises(GameArgumentsValidationError):
            Game(2, 1, {'kings': 3, 'rooks': 2})

    def test_fail_for_null_size_boards(self):
        with self.assertRaises(GameArgumentsValidationError):
            Game(0, 0, {})


class FigureAttackTestCase(unittest.TestCase):
    """ Checking logic of detecting attack cells for various figures """

    @classmethod
    def setUpClass(cls):
        cls.board = Board(Game(4, 4, {}))

    def test_king_attacks(self):
        #     0 1 2 3
        # 0 | * * - -
        # 1 | K * - -
        # 2 | * * - -
        # 3 | - - - -
        test_cells_attack = {(0, 0), (1, 0),
                             (1, 1),
                             (0, 2), (1, 2)}
        test_cells_not_attack = {(2, 0), (3, 0),
                                 (2, 1), (3, 1),
                                 (2, 2), (3, 2),
                                 (0, 3), (1, 3), (2, 3), (3, 3)}
        figure = King(self.board, 0, 1)
        cells_to_attack = set(figure.cells_to_attack())
        self.assertEqual(len(cells_to_attack), 5)
        self.assertSetEqual(cells_to_attack, test_cells_attack)
        assert not cells_to_attack.issubset(test_cells_not_attack)

        #     0 1 2 3
        # 0 | - * * *
        # 1 | - * K *
        # 2 | - * * *
        # 3 | - - - -
        test_cells_attack = {(1, 0), (2, 0), (3, 0),
                             (1, 1), (3, 1),
                             (1, 2), (2, 2), (3, 2)}
        test_cells_not_attack = {(0, 0),
                                 (0, 1),
                                 (0, 2),
                                 (0, 3), (1, 3), (2, 3), (3, 3)}
        figure = King(self.board, 2, 1)
        cells_to_attack = set(figure.cells_to_attack())
        self.assertEqual(len(cells_to_attack), 8)
        self.assertSetEqual(cells_to_attack, test_cells_attack)
        assert not cells_to_attack.issubset(test_cells_not_attack)

    def test_queen_attacks(self):
        #     0 1 2 3
        # 0 | * * - -
        # 1 | Q * * *
        # 2 | * * - -
        # 3 | * - * -
        test_cells_attack = {(0, 0), (1, 0),
                             (1, 1), (2, 1), (3, 1),
                             (0, 2), (1, 2),
                             (0, 3), (2, 3)}
        test_cells_not_attack = {(2, 0), (3, 0),
                                 (2, 2), (3, 2),
                                 (1, 3), (3, 3)}

        figure = Queen(self.board, 0, 1)
        cells_to_attack = set(figure.cells_to_attack())
        self.assertEqual(len(cells_to_attack), 9)
        self.assertSetEqual(cells_to_attack, test_cells_attack)
        assert not cells_to_attack.issubset(test_cells_not_attack)

        #     0 1 2 3
        # 0 | - * * *
        # 1 | * * Q *
        # 2 | - * * *
        # 3 | * - * -
        test_cells_attack = {(1, 0), (2, 0), (3, 0),
                             (0, 1), (1, 1), (3, 1),
                             (1, 2), (2, 2), (3, 2),
                             (0, 3), (2, 3)}
        test_cells_not_attack = {(0, 0),
                                 (0, 2),
                                 (1, 3), (3, 3)}
        figure = Queen(self.board, 2, 1)
        cells_to_attack = set(figure.cells_to_attack())
        self.assertEqual(len(cells_to_attack), 11)
        self.assertSetEqual(cells_to_attack, test_cells_attack)
        assert not cells_to_attack.issubset(test_cells_not_attack)


class FillBoardTestCase(unittest.TestCase):
    """ Checking base game logic (for main usages) """

    @classmethod
    def setUpClass(cls):
        os.environ['TEST_MODE'] = '1'

    def test_simple_board(self):
        # ---------Initial configuration----------
        # Boards dimensions: 3 x 2
        # Figures set:
        #   Kings   :  1
        #   Rooks   :  1
        # -----------------Result-----------------
        # Found 4 combinations:
        # [R] Rook (1;2) | [K] King (3;1)
        #     1 2 3
        # 1 | - - K
        # 2 | R - -
        # --------------------
        # [R] Rook (3;2) | [K] King (1;1)
        #     1 2 3
        # 1 | K - -
        # 2 | - - R
        # --------------------
        # [R] Rook (1;1) | [K] King (3;2)
        #     1 2 3
        # 1 | R - -
        # 2 | - - K
        # --------------------
        # [R] Rook (3;1) | [K] King (1;2)
        #     1 2 3
        # 1 | - - R
        # 2 | K - -
        # --------------------
        combination_1 = [
            {'type': 'Rook', 'pos_x': 0, 'pos_y': 1, 'display_char': 'R'},
            {'type': 'King', 'pos_x': 2, 'pos_y': 0, 'display_char': 'K'},
        ]
        combination_2 = [
            {'type': 'Rook', 'pos_x': 2, 'pos_y': 1, 'display_char': 'R'},
            {'type': 'King', 'pos_x': 0, 'pos_y': 0, 'display_char': 'K'},
        ]
        combination_3 = [
            {'type': 'Rook', 'pos_x': 0, 'pos_y': 0, 'display_char': 'R'},
            {'type': 'King', 'pos_x': 2, 'pos_y': 1, 'display_char': 'K'},
        ]
        combination_4 = [
            {'type': 'Rook', 'pos_x': 2, 'pos_y': 1, 'display_char': 'R'},
            {'type': 'King', 'pos_x': 0, 'pos_y': 0, 'display_char': 'K'},
        ]

        game = Game(3, 2, {'kings': 1, 'rooks': 1})
        game.generate_combinations()
        self.assertEqual(len(game.serialized_boards), 4)
        self.assertIn(combination_1, game.serialized_boards)
        self.assertIn(combination_2, game.serialized_boards)
        self.assertIn(combination_3, game.serialized_boards)
        self.assertIn(combination_4, game.serialized_boards)

    def test_all_figures_combinations(self):
        # ---------Initial configuration----------
        # Boards dimensions: 4 x 4
        # Figures set:
        #  Rooks    :  1
        #  Knights  :  1
        #  Bishops  :  1
        #  Queens   :  1
        #  Kings    :  1
        # -----------------Result-----------------
        # Found 16 combinations:
        # [Q] Queen (3;4) | [B] Bishop (2;1) | [R] Rook (4;2) | [K] King (1;3)
        # | [N] Knight (1;1)
        #     1 2 3 4
        # 1 | N B - -
        # 2 | - - - R
        # 3 | K - - -
        # 4 | - - Q -
        # --------------------
        # [Q] Queen (2;1) | [B] Bishop (3;4) | [R] Rook (1;3) | [K] King (4;2)
        # | [N] Knight (4;4)
        #     1 2 3 4
        # 1 | - Q - -
        # 2 | - - - K
        # 3 | R - - -
        # 4 | - - B N

        # --------------------
        # [Q] Queen (3;1) | [B] Bishop (2;4) | [R] Rook (4;3) | [K] King (1;2)
        # | [N] Knight (1;4)
        #     1 2 3 4
        # 1 | - - Q -
        # 2 | K - - -
        # 3 | - - - R
        # 4 | N B - -
        # --------------------
        # [Q] Queen (2;4) | [B] Bishop (1;2) | [R] Rook (4;3) | [K] King (3;1)
        # | [N] Knight (1;1)
        #     1 2 3 4
        # 1 | N - K -
        # 2 | B - - -
        # 3 | - - - R
        # 4 | - Q - -
        # --------------------

        combination_1 = [
            {'type': 'Queen', 'pos_x': 2, 'pos_y': 3, 'display_char': 'Q'},
            {'type': 'Bishop', 'pos_x': 1, 'pos_y': 0, 'display_char': 'B'},
            {'type': 'Rook', 'pos_x': 3, 'pos_y': 1, 'display_char': 'R'},
            {'type': 'King', 'pos_x': 0, 'pos_y': 2, 'display_char': 'K'},
            {'type': 'Knight', 'pos_x': 0, 'pos_y': 0, 'display_char': 'N'},
        ]
        combination_2 = [
            {'type': 'Queen', 'pos_x': 1, 'pos_y': 0, 'display_char': 'Q'},
            {'type': 'Bishop', 'pos_x': 2, 'pos_y': 3, 'display_char': 'B'},
            {'type': 'Rook', 'pos_x': 0, 'pos_y': 2, 'display_char': 'R'},
            {'type': 'King', 'pos_x': 3, 'pos_y': 1, 'display_char': 'K'},
            {'type': 'Knight', 'pos_x': 3, 'pos_y': 3, 'display_char': 'N'},
        ]
        combination_3 = [
            {'type': 'Queen', 'pos_x': 2, 'pos_y': 0, 'display_char': 'Q'},
            {'type': 'Bishop', 'pos_x': 1, 'pos_y': 3, 'display_char': 'B'},
            {'type': 'Rook', 'pos_x': 3, 'pos_y': 2, 'display_char': 'R'},
            {'type': 'King', 'pos_x': 0, 'pos_y': 1, 'display_char': 'K'},
            {'type': 'Knight', 'pos_x': 0, 'pos_y': 3, 'display_char': 'N'},
        ]
        combination_4 = [
            {'type': 'Queen', 'pos_x': 1, 'pos_y': 3, 'display_char': 'Q'},
            {'type': 'Bishop', 'pos_x': 0, 'pos_y': 1, 'display_char': 'B'},
            {'type': 'Rook', 'pos_x': 3, 'pos_y': 2, 'display_char': 'R'},
            {'type': 'King', 'pos_x': 2, 'pos_y': 0, 'display_char': 'K'},
            {'type': 'Knight', 'pos_x': 0, 'pos_y': 0, 'display_char': 'N'},
        ]

        game = Game(4, 4, {'kings': 1, 'rooks': 1, 'knights': 1, 'queens': 1,
                           'bishops': 1})
        game.generate_combinations()
        self.assertEqual(len(game.serialized_boards), 16)
        self.assertIn(combination_1, game.serialized_boards)
        self.assertIn(combination_2, game.serialized_boards)
        self.assertIn(combination_3, game.serialized_boards)
        self.assertIn(combination_4, game.serialized_boards)


@contextmanager
def capture(command, *args, **kwargs):
    """ Context manager for override sys output from rendering methods """

    out, sys.stdout = sys.stdout, io.StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out


class CaptureLoggingHandler(logging.StreamHandler):
    """ This class helps to capture stdout stream for testing output data
    """

    @property
    def stream(self):
        return sys.stdout

    @stream.setter
    def stream(self, value):
        pass


class RunModeTestCase(unittest.TestCase):
    """ Detect and re-test sys output after rendering all data """

    @classmethod
    def setUpClass(cls):
        cls.logger = logging.getLogger()
        cls.logger.setLevel(logging.INFO)
        # stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler = CaptureLoggingHandler(stream=sys.stdout)
        cls.logger.handlers = [stream_handler]

    def test_render_initial_data(self):
        game = Game(4, 3, {'kings': 3, 'rooks': 2})
        game.logger = self.logger
        with capture(game.render_initial_data) as output:
            msg = 'Boards dimensions: {} x {}'.format(
                game.dimension_x, game.dimension_y
            )
            self.assertIn(msg, output)
            self.assertIn('Kings:3', output.replace(' ', ''))
            self.assertIn('Rooks:2', output.replace(' ', ''))

    def test_run_game_and_render_results(self):
        game = Game(3, 2, {'kings': 1, 'rooks': 1})
        game.logger = self.logger
        with capture(game.run) as output:
            number_of_results = len(game.serialized_boards)
            msg = 'Found {} combinations:'.format(number_of_results)
            self.assertIn(msg, output)
            self.assertEqual(output.count('[K] King'), number_of_results)


if __name__ == '__main__':
    unittest.main()
