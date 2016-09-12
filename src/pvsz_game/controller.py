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
        self.done = False

        self.ev_manager.register(self)
        self.key_event_checks = [self.check_arrows,
                             self.check_quit,
                             self.check_plant]

    def check_arrows(self, event):
        """Move player on board if arrow key has been pressed."""
        ev = None
        if event.key == pygame.K_LEFT:
            ev = events.MoveObject(self.model.player, 'left', 5)
        elif event.key == pygame.K_RIGHT:
            ev = events.MoveObject(self.model.player, 'right', 5)
        elif event.key == pygame.K_UP:
            ev = events.MoveObject(self.model.player, 'up', 1)
        elif event.key == pygame.K_DOWN:
            ev = events.MoveObject(self.model.player, 'down', 1)
        return ev

    def check_plant(self, event):
        """Plant the appropriate type plant on the board."""
        ev = None
        if event.key == pygame.K_1:
            ev = events.GrowPlant('Sunflower', self.model.player.pos)
        return ev

    def check_quit(self, event):
        if event.key == pygame.K_ESCAPE:
            pygame.display.quit()
            pygame.quit()
            self.model.player.alive = False

    def update(self, event):
        if isinstance(event, events.LoopEnd):
            for pygame_event in pygame.event.get():
                if pygame_event.type == pygame.KEYUP:
                    for func in self.key_event_checks:
                        ev = func(pygame_event)
                        if ev:
                            self.ev_manager.post(ev)
                            break