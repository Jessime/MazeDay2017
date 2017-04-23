import argparse

from minesweeper_game.minesweeper import Minesweeper

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument('-v', '--verbose', action='store_true', help='Print information to help with debugging.')
    parser.add_argument('-s', '--size', default=4, type=int, help='Width and height of the board.')
    parser.add_argument('-n', '--n_bombs', default=3, type=int, help='Number of bombs to place on board.')
    parser.add_argument('-po', '--print_only', action='store_true', help='Set if you do not want to use sound-based sentences')
    parser.add_argument('-np', '--no_printing', action='store_true', help='Set if you do not want information printed to the console.')
    args = parser.parse_args()

    app = Minesweeper(print_only=args.print_only,
                      no_printing=args.no_printing,
                      size=args.size,
                      n_bombs=args.n_bombs)

    app.model.run()
