from src.figures import Queen, King, Rook, Bishop, Knight
from .game_logic import Board, Game


def print_attack(figure):
    print('{}'.format(figure.__class__.__name__).center(25, '-'))
    cells = figure.cells_to_attack()
    board = figure.board
    print(cells)
    for y in reversed(range(board.game.dimension_x)):
        res = ''
        for x in range(board.game.dimension_y):
            if (x, y) in cells:
                res += '* '
            elif (x, y) == (figure.pos_x, figure.pos_y):
                res += 'F '
            else:
                res += '- '
        print(res)


def test_attack_lines():
    board = Board(Game(10, 10, {}))
    print_attack(King(board, 0, 2))
    print_attack(Rook(board, 1, 2))
    print_attack(Queen(board, 4, 5))
    print_attack(Bishop(board, 5, 9))
    print_attack(Knight(board, 0, 4))


test_attack_lines()
