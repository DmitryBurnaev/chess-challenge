from src.exceptions import CanNotCreateGameInstance
from src.figures import Queen, King, Rook, Bishop, Knight
from src.game_logic import Board, Game

import unittest


class GameInitialTestCase(unittest.TestCase):

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
        try:
            Game(2, 1, {'kings': 3, 'rooks': 2})
        except CanNotCreateGameInstance as e:
            self.assertIsNotNone(e)
        else:
            raise AssertionError('Created game for fake combinations')

    def test_fail_for_null_size_boards(self):
        try:
            Game(0, 0, {})
        except CanNotCreateGameInstance:
            pass
        else:
            raise AssertionError('Created game null-size board')


class FigureAttackTestCase(unittest.TestCase):

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

    def test_cells_to_attack(self):
        self.assertIsNone(None)
        pass

    def test_fill_board(self):
        pass


if __name__ == '__main__':
    unittest.main()



