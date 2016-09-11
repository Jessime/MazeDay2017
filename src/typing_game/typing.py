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
import pygame

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
        Sets the style of the game. Printing only will have no sounds.
    no_printing : bool (default=False)
        If true, sound will play, but the sentences will not be printed to the console.
    Attributes
    ----------
    sentences : [str] or {str:(int,int)}
        Either raw sentences or sentences as keys to mp3 files.
    play_mp3 : func
        Function used to play the sentence.
    level : int
        Current game level. Number of sentences prompted is equal to level.
    total_words : float
        Words (5 character chunks) in the current sentence.
    avg_accuracy : float
        Accuracy across all sentences in a given level.
    WPM : float
        Raw Words Per Minute typed by player.
    WPM_adjusted : float
        Words Per Minute typed by player and corrected for accuracy.
    WPM_min : int
        Minimum Words Per Minute (adjusted) needed to pass level.
    """
    def __init__(self, num_lvls=5, verbose=False, print_only=False, no_printing=False):
        self.num_lvls = num_lvls
        self.verbose = verbose
        self.print_only = print_only
        self.no_printing = no_printing

        self.sentences = self.load_sentences()
        self.play_mp3 = self.set_mp3_player()
        self.level = 1
        self.total_words = 0.
        self.avg_accuracy = 0.
        self.WPM = None
        self.WPM_adjusted = None
        self.WPM_min = 20

    def load_sentences(self):
        """"Loads appropriate text files for prompt sentences.

        Returns
        -------
        sentences : [str] or {str:(int,int)}
            Either raw sentences or sentences as keys to mp3 files.
        """
        if self.print_only:
            infile = '../data/typing/sentences_clean.txt'
            with open(infile) as infile:
                lines = infile.readlines()
            sentences = [l.lower().strip() for l in lines]
        else:
            infile = '../data/typing/audio_lookup_subset.txt'
            sentences = pickle.load(open(infile, 'rb'))
        return sentences

    def play_linux(self, mp3):
        Popen(['mpg123', '-q', mp3])

    def play_osx(self, mp3):
        Popen(['afplay', mp3])

    def play_windows(self, mp3):
        pygame.mixer.music.load(mp3)
        pygame.mixer.music.play()

    def set_mp3_player(self):
        """Chooses the proper play function based off of the OS.

        Returns
        -------
        play_mp3 : func
            The function used to play the sentence.
        """
        platform = sys.platform
        if self.verbose:
            print('\nPlatform: {}\n'.format(platform))
        if platform == 'linux':
            play_mp3 = self.play_linux
        elif platform == 'darwin':
            play_mp3 = self.play_osx
        elif platform == 'win32':
            play_mp3 = self.play_windows
        return play_mp3

    def hamming_score(self, str1, str2):
        """Typing accuracy based on hamming distance of prompt vs. answer.

        Parameters
        ----------
        str1 : str
            The original sentence, after alignment.
        str2 : str
            The sentence given by the user, after alignment.
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
        """Shows the alignment.

        Parameters
        ----------
        aligned : (str, str)
            Both the original and the input versions of the sentence after alignment.
        """
        print('')
        if self.verbose:
            print(aligned[0])
            print(aligned[1])
            print('')

    def output(self):
        """Gives sentence via print and/or mp3"""
        if self.print_only:
            sentence = random.choice(self.sentences)
        else:
            sentence = random.choice(list(self.sentences.keys()))
            load_info = self.sentences[sentence]
            mp3_file = '../data/typing/{}/{}.mp3'.format(load_info[0], load_info[1])
            self.play_mp3(mp3_file)
        if not self.no_printing:
            print('')
            print(sentence)
        return sentence

    def calc_accuracy(self):
        """"Logic of main loop. Gets input, aligns input, and finds accuracy score."""
        sentence = self.output()
        user_input = input('> ')
        self.total_words += len(sentence)/5
        aligned = align_strings(sentence, user_input)
        self.print_alignment(aligned)
        accuracy = self.hamming_score(aligned[0], aligned[1])
        accuracy /= len(aligned[0])
        self.avg_accuracy += accuracy

    def report_lvl(self, total_time):
        """Show the results of a level.

        Parameters
        ----------
        total_time : float
            The amount of time player spent on current sentence."""
        print('')
        print('Time: {:.2f}s'.format(total_time))
        print('Accuracy: {:.2f}'.format(self.avg_accuracy))
        print('Raw WPM: {:.2f}'.format(self.WPM))
        print('Adjusted WPM: {:.2f}'.format(self.WPM_adjusted))
        print('')

    def update_lvl(self):
        """Reset some variables at the end of a lvl."""
        self.total_words = 0.
        self.avg_accuracy = 0.
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
                print('Please try again! You need a {} WPM to beat this level.'.format(self.WPM_min))
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_lvls', default=5, type=int, help='The number of levels you want to play')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print information to help with debugging.')
    parser.add_argument('-po', '--print_only', action='store_true', help='Set if you do not want to use sound-based sentences')
    parser.add_argument('-np', '--no_printing', action='store_true', help='Set if you do not want the sentences printed to the console.')
    args = parser.parse_args()

    if sys.platform == 'win32':
        pygame.mixer.init(44100)
    game = TypingGame(args.num_lvls, args.verbose, args.print_only, args.no_printing)
    game.run()