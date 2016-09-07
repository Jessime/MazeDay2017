# -*- coding: utf-8 -*-
"""
In the story, imagine that you have to transcribe a conversation some bad guys are having to use at a future time.
For whatever reason, your voice recorder isn't working.
"""

import random
import time
import argparse
import sys
import pickle

from subprocess import Popen

from aligner import align_strings

class TypingGame():
    """"A basic type racing game to measure Words Per Minute.

    Parameters
    ----------
    num_lvls : int (default=3)
        The number of separate rounds to play.
    verbose : bool (default=False)
        If true, additional information will be printed
    print_only : bool (default=False)
        Sets the style of the game. Sound on will provide spoken sentences.

    Attributes
    ----------

    """
    def __init__(self, num_lvls=3, verbose=False, print_only=False, silent=False):
        self.num_lvls = num_lvls
        self.verbose = verbose
        self.print_only = print_only
        self.silent = silent

        self.sentences = self.load_sentences()
        self.play_mp3 = self.set_mp3_player()
        self.level = 1
        self.total_words = 0
        self.avg_accuracy = 0
        self.WPM_min = 20
        self.WPM = None
        self.WPM_adjusted = None

    def load_sentences(self):
        """"Loads appropriate text files for prompt sentences."""
        if self.print_only:
            infile = 'data/typing/sentences_clean.txt'
            with open(infile) as infile:
                lines = infile.readlines()
            sentences = [l.lower().strip() for l in lines]
        else:
            infile = 'data/typing/audio_lookup_subset.txt'
            sentences = pickle.load(open(infile, 'rb'))
        return sentences

    def play_linux(self, mp3):
        Popen(['mpg123', '-q', mp3])

    def play_osx(self, mp3):
        Popen(['afplay', mp3])

    def play_windows(self, mp3):
        pass

    def set_mp3_player(self):
        platform = sys.platform
        if platform == 'linux':
            player = self.play_linux
        if platform == 'darwin':
            player = self.play_osx
        return player

    def hamming_score(self, str1, str2):
        """Typing accuracy based on hamming distance of prompt vs. answer.

        Returns
        -------
        score : int
            Number of chars in prompt which match answer sentence.
        """
        length_difference = abs(len(str1) - len(str2))
        score = sum([1 for s1, s2 in zip(str1, str2) if s1 == s2])
        score += length_difference
        return score

    def pause(self):
        """Wait for approval to move on to the next level."""
        move_on = False
        while not move_on:
            ans = input('Are you ready for level {}? (y/n): '.format(self.level))
            if ans == 'y':
                move_on = True
            elif ans == 'n':
                print('\nSee you next time!\n')
                sys.exit()

    def print_alignment(self, aligned):
        print('')
        if self.verbose:
            print(aligned[0])
            print(aligned[1])

    def output(self):
        if self.print_only:
            sentence = random.choice(self.sentences)
        else:
            sentence = random.choice(list(self.sentences.keys()))
            load_info = self.sentences[sentence]
            mp3_file = 'data/typing/{}/{}.mp3'.format(load_info[0], load_info[1])
            self.play_mp3(mp3_file)
        if not self.silent:
            print('')
            print(sentence)
        return sentence

    def calc_accuracy(self):
        sentence = self.output()
        user_input = input('> ')
        self.total_words += len(sentence)/5
        aligned = align_strings(sentence, user_input)
        self.print_alignment(aligned)
        accuracy = self.hamming_score(aligned[0], aligned[1])
        accuracy /= len(aligned[0])
        self.avg_accuracy += accuracy

    def report_lvl(self, total_time):
        """Show the results of a level."""
        print('')
        print('Time: {:.2f}s'.format(total_time))
        print('Accuracy: {:.2f}'.format(self.avg_accuracy))
        print('Raw WPM: {:.2f}'.format(self.WPM))
        print('Adjusted WPM: {:.2f}'.format(self.WPM_adjusted))
        print('')

    def update_lvl(self):
        """Reset some variables at the end of a lvl."""
        self.total_words = 0
        self.avg_accuracy = 0
        self.level += 1
        self.WPM_min += 10

    def run_level(self):
        """Main loop for an individual level"""
        start = time.time()

        for i in range(self.level):
            self.calc_accuracy()

        total_time = time.time() - start
        self.WPM = 60*self.total_words/total_time
        self.avg_accuracy /= self.level
        self.WPM_adjusted = self.WPM*self.avg_accuracy
        self.report_lvl(total_time)
        self.update_lvl()

    def run(self):
        """Main loop. Runs level and checks for a passing speed."""
        print('Welcome to typer.')
        print('Each round, you will receive an increasing number of sentences.')
        print('Type the sentences as quickly and accurately as possible.')
        print('')
        for i in range(self.num_lvls):
            self.pause()
            self.run_level()
            if self.WPM_adjusted < self.WPM_min:
                print('Sorry, you lose. You need a {} WPM.'.format(self.WPM_min))
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_lvls', default=3, type=int, help='The number of levels you want to play')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print information to help with debugging.')
    parser.add_argument('-po', '--print_only', action='store_true', help='Set if you do not want to use sound-based sentences')
    parser.add_argument('-s', '--silent', action='store_true', help='Set if you do not want the sentences printed to the console.')
    args = parser.parse_args()

    game = TypingGame(args.num_lvls, args.verbose, args.print_only, args.silent)
    game.run()