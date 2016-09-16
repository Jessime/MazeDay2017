# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

import pygame

import events

class BasicView():

    def __init__(self, ev_manager, model):
        self.ev_manager = ev_manager
        self.model = model

        self.clock = pygame.time.Clock()

        self.ev_manager.register(self)

    def update(self, event):
        if isinstance(event, events.LoopEnd):
            self.clock.tick(5)
        elif isinstance(event, events.MoveObject):
            print(event)
            current_square = self.model.board[self.model.player.pos]
            print('Square contains: {}'.format(current_square))
        elif isinstance(event, events.GrowPlant):
            print(event)
        elif isinstance(event, events.CheckBoard):
            print()
            print(self.model.board.items)
            print(self.model.board)
            print()
        elif isinstance(event, events.CheckPlayer):
            print()
            print('Gold: {}'.format(self.model.player.gold))
#            pos = self.model.player.pos
#            print('At: {}: {}'.format(pos, self.model.board[pos]))
            print()
        elif isinstance(event, events.UserQuit):
            print()
            print(event)
        elif isinstance(event, events.SunCollected):
            print()
            print(event)
class AudioView():
    pass # For pygame audio later