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

from pkg_resources import resource_filename
from subprocess import Popen, check_call
from gtts import gTTS

from .aligner import align_strings

class Typer():
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
    skip_intro : bool (default=False)
        If true, intro will not be played. It will still print out.

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
    def __init__(self, num_lvls=5, verbose=False, print_only=False, no_printing=False, skip_intro=False):
        self.num_lvls = num_lvls
        self.verbose = verbose
        self.print_only = print_only
        self.no_printing = no_printing
        self.skip_intro = skip_intro

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
            infile = 'data/sentences_clean.txt'
            with open(infile) as infile:
                lines = infile.readlines()
            sentences = [l.lower().strip() for l in lines]
        else:
            infile = resource_filename('typer_game', 'data/audio_lookup_subset.txt')
            sentences = pickle.load(open(infile, 'rb'))
        return sentences

    def play_linux(self, mp3, pause=False):
        template = resource_filename('typer_game', 'data/{}.mp3'.format(mp3))
        sub = check_call if pause else Popen
        sub(['mpg123', '-q', template])

    def play_osx(self, mp3, pause=False):
        template = resource_filename('typer_game', 'data/{}.mp3'.format(mp3))
        sub = check_call if pause else Popen
        sub(['afplay', template])

    def play_windows(self, mp3, pause=False):
        template = resource_filename('typer_game', 'data/{}.mp3'.format(mp3))
        pygame.mixer.music.load(template)
        pygame.mixer.music.play()
        if pause:
            while pygame.mixer.music.get_busy():
                time.sleep(.1)

    def set_mp3_player(self):
        """Chooses the proper play function based off of the OS.

        Returns
        -------
        play_mp3 : func
            The function used to play the sentence.
        """
        platform = sys.platform
        if platform == 'win32':
            pygame.mixer.init()
        if self.verbose:
            print('\nPlatform: {}\n'.format(platform))
        platform2play = {'linux':self.play_linux,
                         'darwin':self.play_osx,
                         'win32':self.play_windows}
        play_mp3 = platform2play[platform]
        return play_mp3

    def tts_and_play(self, string, pause=True):
        """Translate text to speech and play the mp3.

        Parameters
        ----------
        string : str
            The sentence or words to be spoken.
        """
        template = resource_filename('typer_game', 'data/temp.mp3')
        gTTS(string).save(template)
        self.play_mp3('temp', pause)

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
            prompt = 'Are you ready for level {}? '.format(self.level)
            if self.level < 6:
                self.play_mp3('prompts/{}'.format(self.level))
            ans = input(prompt).lower()
            if ans in ('y', 'yes'):
                move_on = True
            elif ans in ('n', 'no'):
                print('\nSee you next time!\n')
                self.play_mp3('prompts/bye')
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
            mp3_file = '{}/{}'.format(load_info[0], load_info[1])
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
            The amount of time player spent on current sentence.
        """
        results = ('\n'
                   'Time: {} seconds.\n'
                   'Accuracy: {} percent.\n'
                   'Raw words per minute: {}.\n'
                   'Adjusted words per minute: {}.\n'
                   '\n'.format(int(total_time),
                               int(self.avg_accuracy*100),
                               int(self.WPM),
                               int(self.WPM_adjusted)))
        print(results)
        self.tts_and_play(results)

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
        intro = ('Welcome to typer.\n'
                 'Each round, you will receive an increasing number of sentences.\n'
                 'Be ready, there are no pauses between sentences.\n'
                 'Also, you can start typing as soon as you want.\n'
                 'You do not need to wait for the sentence to finish.\n'
                 'Type the sentences as quickly and accurately as possible.\n'
                 'To make things easier, there will be no upper case characters.\n'
                 'But there will be punctuation in the middle and end of sentences.\n')
        print(intro)
        if not self.skip_intro:
            self.play_mp3('prompts/intro', pause=True)
        for i in range(self.num_lvls):
            self.pause()
            self.run_level()
            if self.WPM_adjusted < self.WPM_min:
                prompt = 'Please try again! You need {} words per minute to beat this level.'.format(self.WPM_min)
                print(prompt)
                self.tts_and_play(prompt)
                break
