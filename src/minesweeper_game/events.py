# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime

These Events are in alphabetical order.
"""

class ButtonPress():

    def __init__(self, button):
        self.button = button

class ChangePos():

    def __init__(self, button):
        self.button = button

class CheckBoard():
    def __init__(self): pass
    def __str__(self): return 'Show the current state of the board.'

class CheckPlayer():
    def __init__(self): pass
    def __str__(self): return 'Show the current state of the Player.'

class CountUnflagged():
    pass

class Explode():

    def __init__(self):
        self.filename = 'explosion'

class FlagNum():

    def __init__(self, num):
        self.num = num

class Init():
    def __init__(self): pass
    def __str__(self): return 'Starting app.'

class LoopEnd():

    def __init__(self):
        self.name = 'LoopEnd'

class ToggleFlag():

    def __init__(self):
        self.filename = 'buzz2'

class TryButtonPress():

    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return str(self.pos)

class TryChangePos():

    def __init__(self, direction):
        self.direction = direction

    def __str__(self):
        return self.direction

class TryFlagToggle():

    def __init__(self, pos):
        self.pos = pos

class UserQuit():
    def __init__(self): pass
    def __str__(self): return 'Thanks for playing! We hope you enjoyed it.'

class Win():
    def __init__(self):
        self.filename = 'cheer'

    def __str__(self):
        return 'Wow, you made it out alive! Good job!'

class EventManager():

    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def post(self, event):
        for listener in self.listeners:
            listener.notify(event)
