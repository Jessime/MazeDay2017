# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime

These Events are in alphabetical order.
"""

class Init():
    def __init__(self): pass
    def __str__(self): return 'Starting app.'

class LoopEnd():

    def __init__(self):
        self.name = 'LoopEnd'

class UserQuit():
    def __init__(self): pass
    def __str__(self): return 'Thanks for playing! We hope you enjoyed it.'

class Flip():
    def __init__(self):
        self.string = string
    def test(self, string):
        if self.string == 'l':
            # self.flip_left == 'l'
            pass
        elif self.string == 'r':
            # self.flip_rigt == 'r'
            pass
        # self.string = None
    #     self.flip_left = None
    #     self.flip_rigt = None
    # def notify(self):
    # if self.string == 'l':
    #     self.flip_left == 'l'
    # elif self.string == 'r':
    #     self.flipper_right == 'r'
    # def flip_left(self):
    #     self.components.flipper_left.flip_up = True
    #
    # def flip_right(self):
    #     self.components.flipper_right.flip_up = True

class EventManager():

    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def post(self, event):
        for listener in self.listeners:
            listener.notify(event)
