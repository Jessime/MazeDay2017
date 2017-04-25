# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

import os
import pygame

from pkg_resources import resource_filename
from random import choice
from string import ascii_lowercase
from time import sleep
from gtts import gTTS

class View:

    def __init__(self, ev_manager, model):
        self.ev_manager = ev_manager
        self.model = model

        self.event = None

        self.ev_manager.register(self)

    def notify(self, event):
        self.event = event
        name = event.__class__.__name__
        if name == 'Stats':
            print(event.string)
        if name in self.event_func_dict:
            self.event_func_dict[name]()

class BasicView(View):

    def __init__(self, ev_manager, model, no_printing):
        super().__init__(ev_manager, model)
        self.no_printing = no_printing
        self.clock = pygame.time.Clock()
        self.event_func_dict = {'CheckBoard': self.check_board,
                                'CheckPlayer': self.check_player,
                                'DeathByZombie': self.show,
                                'GrowPlant': self.show,
                                'MoveHome': self.show,
                                'Init': self.initialize,
                                'LoopEnd': self.loop_end,
                                'NoGold':self.show,
                                'PlayerMoves': self.player_moves,
                                'SunCollected': self.show,
                                'UserQuit': self.exit_game,
                                'Win':self.show}

    def check_board(self):
        self.show(self.model.board.items)
        self.show(self.model.board)

    def check_player(self):
        self.show('Gold: {}'.format(self.model.player.gold))

    def exit_game(self):
        pygame.display.quit()
        pygame.quit()
        self.show()

    def initialize(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_mode([100, 100])

    def loop_end(self):
        self.clock.tick(20)

    def player_moves(self):
        self.show()
        current_square = self.model.board[self.model.player.pos]
        self.show('Square contains: {}'.format(current_square))

    def show(self, string=''):
        if not self.no_printing:
            if string:
                print('\n', string, '\n')
            else:
                print('\n', self.event, '\n')


class AudioView(View):

    def __init__(self, ev_manager, model):
        super().__init__(ev_manager, model)

        self.previous_player_row = None
        self.event_func_dict = {'CheckBoard': self.check_board,
                                'CheckInPos': self.check_in_pos,
                                'CheckPlayer': self.tts_and_play,
                                'DeathByZombie': self.play,
                                'Explosion': self.play,
                                'GrowPlant': self.play,
                                'MoveHome': self.play,
                                'InitLevel': self.play,
                                'NoGold':self.play,
                                'PlayerMoves': self.player_moves,
                                'SunCollected': self.play,
                                'TogglePause' : self.toggle_pause,
                                'UserQuit': self.show}

    def check_board(self):
        for row_num in range(5):
            zombie_count = self.model.board.zombies_in_row(row_num)
            self.play('there_are')
            self.play(str(zombie_count))
            self.play('zombie_row')
            self.play(str(row_num))
            if zombie_count > 0:
                zombie_col = self.model.board.first_zombie_col(row_num)
                self.play('starting_at')
                self.tts_and_play(str(zombie_col))

    def check_in_pos(self):
        square = self.model.board[self.model.player.pos]
        if square:
            self.play(square[0].noise)
            self.tts_and_play('Health is {}.'.format(square[0].health))

    def show(self): pass

    def player_moves(self):
        self.play()
        row = self.model.player.pos[0]
        if row != self.previous_player_row:
            self.previous_player_row = row
            zombie_col = self.model.board.first_zombie_col(row)
            if zombie_col is not None:
                volume = (100 - zombie_col)/100
                pygame.mixer.music.set_volume(volume)
                self.play('zombie')
                pygame.mixer.music.set_volume(100)

    def toggle_pause(self):
        if self.model.paused:
            self.play('pause')
        else:
            self.play('resume')


    def skip_on_busy(self):
        """Decides if mp3 should play or not.

        Returns
        -------
        skip : bool
            If True, mp3 file will not play
        """
        skip = False
        try:
            check_busy = self.event.check_busy
        except AttributeError:
            check_busy = False
        if check_busy and pygame.mixer.music.get_busy():
            skip = True
        return skip

    def check_pause_gameplay(self):
        """Decide if game should be slept until mp3 is finished"""
        try:
            pause = self.event.pause_gameplay
        except AttributeError:
            pause = False
        if pause:
            while pygame.mixer.music.get_busy():
                sleep(.01)

    def play(self, filename=None):
        """Play the event mp3.

        Paramters
        ---------
        filename : str
            If filename is past, the corresponding mp3 file will be played instead of self.event.mp3.
        """
        if filename is None:
            filename = self.event.mp3
        if filename == '': #TODO fix this
            return

        if self.skip_on_busy():
            return

        filename = resource_filename('pvsz_game', 'data/{}.mp3'.format(filename))
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        self.check_pause_gameplay()
    #
    # def clean(self, filename):
    #     """Remove temporary file when it is freed"""
    #     print(filename)
    #     pygame.mixer.quit()
    #     sleep(.1)
    #     os.remove(filename)
    #     pygame.mixer.init()

    def tts_and_play(self, string=''):
        """Uses Google's text-to-speech to play a string

        Parameters
        ----------
        string : str (default='')
            Sentence or phrase to be spoken.
        """
        if not string:
            string = self.event.string
        fake = resource_filename('pvsz_game', 'data/1.mp3') #TODO hack shouldn't have to load fake file
        pygame.mixer.music.load(fake)
        template = resource_filename('pvsz_game', 'data/temp.mp3')
        gTTS(string).save(template)
        self.play('temp')
