# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

import pygame
import pvsz_game.events as events
import inspect

class Controller():

    def __init__(self, ev_manager, model):
        self.ev_manager = ev_manager
        self.model = model
        self.done = False

        self.ev_manager.register(self)
        self.key_event_checks = [self.check_arrows,
                                 self.check_state_checks,
                                 self.check_plant,
                                 self.check_others]
        self.key2plant = {pygame.K_1:'Sunflower',
                          pygame.K_2:'PeaShooter',
                          pygame.K_3:'CherryBomb',
                          pygame.K_4:'WallNut',
                          pygame.K_5:'SnowPea'}


    def check_arrows(self, message, event):
        """Move player on board if arrow key has been pressed."""
        if event.key == pygame.K_LEFT:
            message = events.PlayerMoves(self.model.player, 'left', 5)
        elif event.key == pygame.K_RIGHT:
            message = events.PlayerMoves(self.model.player, 'right', 5)
        elif event.key == pygame.K_UP:
            message = events.PlayerMoves(self.model.player, 'up', 1)
        elif event.key == pygame.K_DOWN:
            message = events.PlayerMoves(self.model.player, 'down', 1)
        return message

    def check_plant(self, message, event):
        """Plant the appropriate type plant on the board."""
        if event.key in self.key2plant:
            message = events.TryPlanting(self.key2plant[event.key], self.model.player.pos)
        return message

    def check_others(self, message, event):
        if event.key == pygame.K_ESCAPE:
            message = events.UserQuit()
        elif event.key == pygame.K_SPACE:
            message = events.TryCollecting(self.model.player.pos)
        elif event.key == pygame.K_h:
            message = events.MoveHome()
        elif event.key == pygame.K_p:
            message = events.TogglePause()
        return message

    def toggle_pause(self):
        """If game paused, send no events until game is unpaused"""
        message = None
        print('paused: ', self.model.paused)
        print('\n'*2)
        #print('caller: ', inspect.getouterframes(inspect.currentframe(), 2)[1][3])
        #print('caller: ', inspect.getouterframes(inspect.currentframe(), 2))
        while self.model.paused:
            for pygame_event in pygame.event.get():
                print('event: ', pygame_event)
                if pygame_event.type == pygame.KEYDOWN:
                    message = self.check_others(message, pygame_event)
                    print(message.__class__.__name__)
            if isinstance(message, events.TogglePause):
                self.ev_manager.post(message)

    def check_state_checks(self, message, event):
        """Presents information about current state of game."""
        if event.key == pygame.K_b:
            message = events.CheckBoard()
        if event.key == pygame.K_m:
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

        elif isinstance(event, events.TogglePause):
            self.toggle_pause()
