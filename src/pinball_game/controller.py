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

    def down_keys(self, message, event):
        if event.key == pygame.K_ESCAPE:
            message = events.UserQuit()
        elif event.key == pygame.K_f:
            message = events.PressedBin(0)
        elif event.key == pygame.K_j:
            message = events.PressedBin(1)
        return message

    def up_keys(self, message, event):
        if event.key == pygame.K_SPACE:
            message = events.Launch()
        return message

    def pressed_keys(self, message, keys):
        if keys[pygame.K_SPACE]:
            message = events.PowerLaunch()
        return message

    def notify(self, event):
        if isinstance(event, events.LoopEnd):
            message = None
            keys = pygame.key.get_pressed()
            message = self.pressed_keys(message, keys)
            if message:
                self.ev_manager.post(message)

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
