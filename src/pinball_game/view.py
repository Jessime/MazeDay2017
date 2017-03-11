# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

import pygame

class View:

    def __init__(self, ev_manager, model):
        self.ev_manager = ev_manager
        self.model = model

        self.event = None

        self.ev_manager.register(self)

    def notify(self, event):
        self.event = event
        name = event.__class__.__name__
        if name in self.event_func_dict:
            self.event_func_dict[name]()

class BasicView(View):

    def __init__(self, ev_manager, model):
        super().__init__(ev_manager, model)

        self.clock = pygame.time.Clock()
        self.event_func_dict = {'Init': self.initialize,
                                'LoopEnd': self.loop_end,
                                'UserQuit': self.exit_game}

    def exit_game(self):
        pygame.display.quit()
        pygame.quit()
        self.show()

    def initialize(self):
        print(str(self.event))
        pygame.init()
        pygame.display.set_mode([100, 100])

    def loop_end(self):
        self.clock.tick(20)

    def show(self):
        print('\n', self.event, '\n')
