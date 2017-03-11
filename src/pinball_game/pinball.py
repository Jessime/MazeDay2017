# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 23:14:44 2016

@author: jessime
"""
import time

import events
from controller import Controller
from view import BasicView

class Model():

    def __init__(self, ev_manager):
        self.ev_manager = ev_manager

        self.loop_start = time.time()
        self.loop_time = 0
        self.running = True

        self.ev_manager.register(self)

    def exit_game(self):
        self.running = False

    def notify(self, event):
        if isinstance(event, events.LoopEnd):
            self.loop_time = time.time() - self.loop_start
            self.loop_start = time.time()
        elif isinstance(event, events.UserQuit):
            self.exit_game()

    def update(self):
        '''All game logic.'''
        pass

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
