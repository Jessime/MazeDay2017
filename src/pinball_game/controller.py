# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

import pygame
import events

class Controller():

    def __init__(self, ev_manager, model):
        self.ev_manager = ev_manager
        self.model = model

        self.ev_manager.register(self)
        self.key_event_checks = [self.check_others]

    def check_others(self, message, event):
        if event.key == pygame.K_ESCAPE:
            message = events.UserQuit()
        elif event.key == pygame.K_f:
            # message = flipper_left.flip_up = True # events.MoveFlipper()
            message = events.Flip('l')
        elif event.key == pygame.K_j:
            message = events.Flip('r')
        return message

    def notify(self, event):
        if isinstance(event, events.LoopEnd):
            for pygame_event in pygame.event.get():
                message = None
                if pygame_event.type == pygame.KEYUP:
                    for func in self.key_event_checks:
                        message = func(message, pygame_event)
                        if message:
                            self.ev_manager.post(message)
                            break
