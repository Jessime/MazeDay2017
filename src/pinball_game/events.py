# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime

These Events are in alphabetical order.
"""
class Collision():
    def __init__(self, mp3):
        self.mp3 = mp3

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
    def __init__(self, side):
        self.side = side

class GameOver():
    def __init__(self): pass
    def __str__(self): return 'Game over, better luck next time!'

class Launch():
    def __init__(self): pass

class PowerLaunch():
    def __init__(self):
        pass

class PressedBin():
    def __init__(self, num):
        self.num = num

class PressedBinEval():
    def __init__(self, num, result):
        self.num = num
        self.result = result

class EventManager():
    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def post(self, event):
        for listener in self.listeners:
            listener.notify(event)
