# -*- coding: utf-8 -*-
"""
In the story, imagine that you have to transcribe a conversation some bad guys are having to use at a future time.
For whatever reason, your voice recorder isn't working.
"""

import random
import time
import argparse
import sys

from aligner import align_strings

class TypingGame():
    """"A basic type racing game to measure Words Per Minute.

    Parameters
    ----------
    num_lvls : int (default=3)
        The number of separate rounds to play.
    verbose : bool (default=False)
        If true, additional information will be printed
    silent : bool (default=False)
        Sets the style of the game. Sound on will provide spoken sentences.

    Attributes
    ----------

    """
    def __init__(self, num_lvls=3, verbose=False, silent=False):
        self.num_lvls = num_lvls
        self.verbose = verbose
        self.silent = silent

        self.sentences = self.load_sentences()
        self.level = 1
        self.WPM_min = 20
        self.WPM_adjusted = None

    def load_sentences(self):
        """"Loads appropriate text files for prompt sentences."""
        infile = 'data/sentences_clean.txt'
        with open(infile) as infile:
            lines = infile.readlines()
        lines = [l.lower().strip() for l in lines]
        return lines

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

    def run_level(self):
        """Main loop for an individual level"""
        total_words = 0
        avg_correction = 0
        start = time.time()

        for i in range(self.level):
            sentence = random.choice(self.sentences)
            total_words += len(sentence)/5
            print('')
            print(sentence)
            user_input = input('> ')
            print('')
            aligned = align_strings(sentence, user_input)
            if self.verbose:
                print(aligned[0])
                print(aligned[1])
            correction = self.hamming_score(aligned[0], aligned[1])
            correction /= len(aligned[0])
            avg_correction += correction

        total_time = time.time() - start
        WPM = 60*total_words/total_time
        avg_correction /= self.level
        self.WPM_adjusted = WPM*avg_correction
        self.level += 1
        self.WPM_min += 10
        print('Time: {:.2f}s'.format(total_time))
        print('Accuracy: {:.2f}'.format(avg_correction))
        print('Raw WPM: {:.2f}'.format(WPM))
        print('Adjusted WPM: {:.2f}'.format(self.WPM_adjusted))
        print('')

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
    parser.add_argument('-s', '--silent', action='store_true', help='Set if you do not want to use sound-based sentences')
    args = parser.parse_args()

    game = TypingGame(args.num_lvls, args.verbose)
    game.run()