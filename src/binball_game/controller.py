# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

import pygame
import time
import binball_game.events as events

class Controller():
    def __init__(self, ev_manager, model):
        self.ev_manager = ev_manager
        self.model = model

        self.ev_manager.register(self)
        self.key_event_checks = [self.down_keys]
        bin_keys = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
        self.bin_map = dict(zip(bin_keys, range(4)))

    def down_keys(self, message, event):
        if event.key == pygame.K_ESCAPE:
            message = events.UserQuit()
        elif event.key in self.bin_map:
            message = events.PressedBin(self.bin_map[event.key])
        elif event.key == pygame.K_b:
            message = events.Lives(self.model.player_lives)
        elif event.key == pygame.K_p:
            message = events.TogglePause()
        elif event.key == pygame.K_t:
            message = events.TestNotes()
        elif event.key == pygame.K_r:
            message = events.CheckCoinBonus(time.time())
        return message

    def up_keys(self, message, event):
        if event.key == pygame.K_SPACE:
            message = events.Launch()
        return message

    def pressed_keys(self, message, keys):
        if keys[pygame.K_SPACE]:
            message = events.PowerLaunch()
        return message

    def toggle_pause(self):
        """If game paused, send no events until game is unpaused"""
        message = None
        while self.model.paused:
            for pygame_event in pygame.event.get():
                print('event: ', pygame_event)
                if pygame_event.type == pygame.KEYDOWN:
                    message = self.down_keys(message, pygame_event)
            if isinstance(message, events.TogglePause):
                self.ev_manager.post(message)

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

        elif isinstance(event, events.TogglePause):
            self.toggle_pause()
