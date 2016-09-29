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
        self.key_event_checks = [self.check_arrows,
                                 self.check_others,
                                 self.check_state]

    def check_arrows(self, message, event):
        """Move player on board if arrow key has been pressed."""
        if event.key == pygame.K_LEFT:
            message = events.TryChangePos('left')
        elif event.key == pygame.K_RIGHT:
            message = events.TryChangePos('right')
        elif event.key == pygame.K_UP:
            message = events.TryChangePos('up')
        elif event.key == pygame.K_DOWN:
            message = events.TryChangePos('down')
        return message

    def check_others(self, message, event):
        if event.key == pygame.K_ESCAPE:
            message = events.UserQuit()
        elif event.key == pygame.K_SPACE:
            message = events.TryButtonPress(self.model.pos)
        elif event.key == pygame.K_f:
            message = events.TryFlagToggle(self.model.pos)
        return message

    def check_state(self, message, event):
        if event.key == pygame.K_b:
            message = events.CheckBoard()
        elif event.key == pygame.K_m:
            message = events.CheckPlayer()
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