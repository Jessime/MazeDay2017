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
        if ev is not None:
            self.ev_manager.post(ev)

    def check_quit(self, event):
        if event.key == pygame.K_ESCAPE:
            pygame.display.quit()
            pygame.quit()
            self.model.player.alive = False

    def update(self, event):
        if isinstance(event, events.LoopEnd):
            for ev in pygame.event.get():
                if ev.type == pygame.KEYUP:
                    self.check_arrows(ev)
                #self.check_quit(event)