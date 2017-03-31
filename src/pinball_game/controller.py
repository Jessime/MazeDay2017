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
        self.key_event_checks = [self.down_keys]

        self.power = 0

    def down_keys(self, message, event):
        if event.key == pygame.K_ESCAPE:
            message = events.UserQuit()
        elif event.key == pygame.K_f:
            message = events.Flip('l')
        elif event.key == pygame.K_j:
            message = events.Flip('r')
        return message

    def up_keys(self, message, event):
        if event.key == pygame.K_SPACE:
            if not self.model.islaunched:
                message = events.PowerLaunch(self.power)
        return message

    def pressed_keys(self, keys):
        if keys[pygame.K_SPACE]:
            if not self.model.islaunched:
                self.power += 1

    def notify(self, event):
        if isinstance(event, events.LoopEnd):
            message = None
            keys = pygame.key.get_pressed()
            self.pressed_keys(keys)
            for pygame_event in pygame.event.get():
                message = None
                if pygame_event.type == pygame.KEYDOWN:
                    for func in self.key_event_checks:
                        message = func(message, pygame_event)
                elif pygame_event.type == pygame.KEYUP:
                    message = self.up_keys(message, pygame_event)
                elif pygame_event.type == pygame.QUIT:
                    message = events.UserQuit()
                if message:
                    self.ev_manager.post(message)
                    break
