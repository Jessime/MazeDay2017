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

class Flip_l():                 #???
    def __init__(self): pass
        # self.name = 'l'

class Flip_r():                 #???
    def __init__(self): pass
        # self.name = 'r'

class EventManager():
    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def post(self, event):
        for listener in self.listeners:
            listener.notify(event)
