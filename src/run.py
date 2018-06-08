"""
This module helps to run game logic gor specific attributes:
position arguments:
    Dimension X
    Dimension Y
keyword arguments:
    --kings: Number of Kings
    --queens: Number of Queens
    --rooks: Number of Rooks
    --bishops: Number of Bishops
    --knights: Number of Knights

Example:
    python3 src.run 3 4 --kings 3 --bishops 2

You can get additional information by using:

$ python3 -m src.run --help

"""
import argparse

from src.game_logic import Game
from src.logging_config import get_logger

if __name__ == '__main__':
    logger = get_logger(__name__)

    p = argparse.ArgumentParser()
    p.add_argument('dimension_x', metavar='Dimension X', type=int,
                   choices=range(1, 9),
                   help='Number of cells by X: like A,B,C,D ... N')
    p.add_argument('dimension_y', metavar='Dimension Y', type=int,
                   choices=range(1, 9),
                   help='Number of cells by Y: like 1,2,3,4 ... M')

    p.add_argument('--kings', type=int, default=0, help='Number of Kings')
    p.add_argument('--queens', type=int, default=0, help='Number of Queens')
    p.add_argument('--rooks', type=int, default=0, help='Number of Rooks')
    p.add_argument('--bishops', type=int, default=0, help='Number of Bishops')
    p.add_argument('--knights', type=int, default=0, help='Number of Knights')

    p.add_argument('--file', default=False, action='store_true',
                   help='To write result to file')
    args = p.parse_args()

    total_figure_numbers = sum(
        [args.kings, args.queens, args.rooks, args.bishops, args.knights]
    )

    if total_figure_numbers == 0:
        logger.critical('Total numbers of figures must be greater than 0.\n'
                        'Please, specify other arguments for needed '
                        'combinations.')
        exit(1)
    else:
        if total_figure_numbers >= (args.dimension_x * args.dimension_y):
            logger.critical('The number of figures is greater than the '
                            'dimension of the board. \nPlease, specify other '
                            'arguments for needed combinations.')
            exit(1)

    figures_set = {
        'kings': args.kings,
        'queens': args.queens,
        'rooks': args.rooks,
        'bishops': args.bishops,
        'knights': args.knights
    }
    game = Game(args.dimension_x, args.dimension_y, figures_set,
                result_to_file=args.file)
    game.run()
