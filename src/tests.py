from .game_logic import Board, King, Rock, Game


def test_attack_lines():
    board = Board(Game(3,3))
    k = King(board, 1, 2)
    r = Rock(board, 1, 2)
    print('Rock attack')
    print(r.cells_to_attack())
    print('King attack')
    print(k.cells_to_attack())