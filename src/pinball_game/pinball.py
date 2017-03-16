# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 23:14:44 2016

@author: jessime
"""
import time

import events
from controller import Controller
from view import BasicView
import components

class Model():
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager

        self.loop_start = time.time()
        self.loop_time = 0
        self.running = True

        self.ev_manager.register(self)

        self.width = 400
        self.height = 800

        self.components_list = []
        self.ball = components.Particle(250,300,15)

        self.flipper_left = components.Flipper(75,700,125,730,75,650)
        self.flipper_right = components.Flipper(325,700,275,730,325,650)

        self.event = None

    def exit_game(self):
        self.running = False

    def flip(self):
        if self.event.side == 'l':
            self.flipper_left.flip_up = True
        elif self.event.side == 'r':
            self.flipper_right.flip_down = True

    def notify(self, event):
        self.event = event
        if isinstance(event, events.LoopEnd):
            self.loop_time = time.time() - self.loop_start
            self.loop_start = time.time()
        elif isinstance(event, events.UserQuit):
            self.exit_game()
        elif isinstance(event, events.Flip):
            self.flip()

    def update(self):
        '''All game logic.'''
        self.ball.move()
        self.ball.bounce(self.width,self.height)
        self.flipper_left.update()
        self.flipper_right.update()

    def run(self):
        self.ev_manager.post(events.Init())
        while self.running:
            self.update()
            self.ev_manager.post(events.LoopEnd())

class App():
    def __init__(self, print_only=False, no_printing=False):
        self.ev_manager = events.EventManager()
        self.model = Model(self.ev_manager)
        self.controller = Controller(self.ev_manager, self.model)
        self.basic_view = BasicView(self.ev_manager, self.model)

if __name__ == '__main__':

    app = App()
    app.model.run()
