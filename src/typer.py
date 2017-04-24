import argparse

from typer_game.typer import Typer

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_lvls', default=5, type=int, help='The number of levels you want to play')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print information to help with debugging.')
    parser.add_argument('-po', '--print_only', action='store_true', help='Set if you do not want to use sound-based sentences')
    parser.add_argument('-np', '--no_printing', action='store_true', help='Set if you do not want the sentences printed to the console.')
    parser.add_argument('-s', '--skip_intro', action='store_true', help='Set if you do not want to listen to the intro.')
    args = parser.parse_args()

    game = Typer(args.num_lvls,
                      args.verbose,
                      args.print_only,
                      args.no_printing,
                      args.skip_intro)
    game.run()
