# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

import pygame

class BasicView():

    def __init__(self, ev_manager, model):
        self.ev_manager = ev_manager
        self.model = model

        self.event = None
        self.clock = pygame.time.Clock()
        self.event_func_dict = {'LoopEnd': self.loop_end,
                                'MoveObject': self.move_object,
                                'GrowPlant': self.show,
                                'CheckBoard': self.check_board,
                                'CheckPlayer': self.check_player,
                                'UserQuit': self.show,
                                'SunCollected': self.show}

        self.ev_manager.register(self)

    def check_board(self):
        print('\n', self.model.board.items)
        print(self.model.board, '\n')

    def check_player(self):
        print('\n', 'Gold: {}'.format(self.model.player.gold), '\n')

    def loop_end(self):
        self.clock.tick(20)

    def move_object(self):
        print(self.event)
        current_square = self.model.board[self.model.player.pos]
        print('Square contains: {}'.format(current_square))

    def show(self):
        print('\n', self.event, '\n')

    def update(self, event):
        self.event = event
        name = event.__class__.__name__
        if name in self.event_func_dict:
            self.event_func_dict[name]()

class AudioView():
    pass # For pygame audio later