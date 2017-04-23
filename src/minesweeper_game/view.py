# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

import pygame
from time import sleep
from pkg_resources import resource_filename

class View:

    def __init__(self, ev_manager, model):
        self.ev_manager = ev_manager
        self.model = model

        self.clock = pygame.time.Clock()
        self.event = None

        self.ev_manager.register(self)

    def notify(self, event):
        self.event = event
        name = event.__class__.__name__
        if name in self.event_func_dict:
            self.event_func_dict[name]()

class BasicView(View):

    def __init__(self, ev_manager, model):
        super().__init__(ev_manager, model)

        self.event_func_dict = {'ButtonPress' : self.check_board,
                                'ChangePos' : self.change_pos,
                                'CheckBoard': self.check_board,
                                'CheckPlayer': self.check_player,
                                'Explode' : self.check_board,
                                'Init': self.initialize,
                                'LoopEnd' : self.loop_end,
                                'UserQuit' : self.exit_game,
                                'Win' : self.show}

    def change_pos(self):
        print('\n', 'Pos: {}'.format(self.model.pos), '\n')

    def check_board(self):
        print(len(self.model.board))
        print('\n'+' '*4+', '.join(map(str, range(len(self.model.board)))))
        print('\n'.join(['{}: {}'.format(i, row) for i, row in enumerate(self.model.board)]))

    def check_player(self):
        print('\n', 'Pos: {}'.format(self.model.pos), '\n')

    def exit_game(self):
        pygame.display.quit()
        pygame.quit()
        self.show()

    def initialize(self):
        pygame.init()
        pygame.display.set_mode([100, 100])

    def loop_end(self):
        self.clock.tick(20)

    def show(self):
        print('\n', self.event, '\n')


class AudioView(View):

    def __init__(self, ev_manager, model):
        super().__init__(ev_manager, model)

        self.previous_player_col = None
        self.event_func_dict = {'ButtonPress' : self.button_press,
                                'ChangePos' : self.change_pos,
                                'CheckPlayer' : self.check_player,
                                'Explode' : self.play,
                                'FlagNum' : self.flag_num,
                                'Init': self.initialize,
                                'LoopEnd' : self.loop_end,
                                'ToggleFlag' : self.play,
                                'Win' : self.play}

    def button_press(self):
        self.play()
        if not self.event.button.is_bomb:
            self.play(str(self.event.button.number))

    def change_pos(self):
        self.play()
        if self.model.has_pressed:
            if self.event.button.is_flagged:
                self.play('buzz')
            if not self.event.button.is_hidden:
                self.play(str(self.event.button.number))

    def check_player(self):
        self.play(str(self.model.pos[0]))
        self.play(str(self.model.pos[1]))

    def flag_num(self):
        self.play(str(self.event.num))

    def initialize(self):
        pygame.init()
        pygame.display.set_mode([100, 100])

    def loop_end(self):
        self.clock.tick(20)

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
        if filename is None:
            filename = self.event.filename
        pkg = 'minesweeper_game'
        template = resource_filename(pkg, 'data/{}.mp3'.format(filename))
        pygame.mixer.music.load(template)
        pygame.mixer.music.play()

        self.check_pause_gameplay()
