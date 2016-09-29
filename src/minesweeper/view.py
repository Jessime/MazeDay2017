# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

import pygame
from subprocess import Popen, check_call

class View:

    def __init__(self, ev_manager, model):
        self.ev_manager = ev_manager
        self.model = model

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

        self.clock = pygame.time.Clock()
        self.event_func_dict = {'ButtonPress' : self.check_board,
                                'ChangePos' : self.change_pos,
                                'CheckBoard': self.check_board,
                                'CheckPlayer': self.check_player,
                                'Init': self.initialize,
                                'LoopEnd': self.loop_end,
                                'UserQuit': self.exit_game}

    def change_pos(self):
        print('\n', 'Pos: {}'.format(self.model.pos), '\n')

    def check_board(self):
        print('    0, 1, 2, 3, 4. 5, 6, 7')
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
                                'ChangePos': self.change_pos}

    def button_press(self):
        cmd = 'mpg123 -q data/press.mp3'.split()
        check_call(cmd)
        cmd = ''

    def change_pos(self):
        cmd = 'mpg123 -q data/move.mp3'.split()
        check_call(cmd)
        if self.event.button is not None:
            if not self.event.button.is_hidden:
                num = self.event.button.number
                if num != 0:
                    cmd = 'mpg123 -q data/{}.mp3'.format(num).split()
                    check_call(cmd)