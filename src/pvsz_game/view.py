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
            self.clock.tick(20)
        elif isinstance(event, events.MoveObject):
            print(event)


class AudioView():
    pass # For pygame audio later
