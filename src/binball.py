from binball_game.binball import App
import os
import argparse

if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    parser = argparse.ArgumentParser()
    parser.add_argument('-ns', '--no_sound', action='store_false')
    parser.add_argument('-nv', '--no_video', action='store_false')
    choices = ['easy','regular','hard','veteran']
    parser.add_argument('-d', '--difficulty', choices=choices, default='regular')
    args = parser.parse_args()
    app = App(args.no_sound, args.no_video, args.difficulty)
    app.model.run()
