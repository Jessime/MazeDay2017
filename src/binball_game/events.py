# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime

These Events are in alphabetical order.
"""
class Collision():
    def __init__(self, mp3, pause_gameplay=False):
        self.mp3 = mp3
        self.pause_gameplay = pause_gameplay

class Init():
    def __init__(self): pass
    def __str__(self): return 'Starting app.'

class LoopEnd():
    def __init__(self):
        self.name = 'LoopEnd'

class UserQuit():
    def __init__(self): pass
    def __str__(self): return 'Thanks for playing! We hope you enjoyed it.'

class FailedLaunch():
    def __init__(self):
        self.mp3 = 'launch_error'

# class Flip():
#     def __init__(self, side):
#         self.side = side

class GameOver():
    def __init__(self): pass
    def __str__(self): return 'Game over, better luck next time!'

class Launch():
    def __init__(self):
        self.mp3 = 'launch'

class LifeLost():
    def __init__(self):
        self.mp3 = 'lose1'
        self.pause_gameplay = True

class Lives():
    def __init__(self, lives):
        self.lives  = lives
        self.mp3 = str(lives)

    def __repr__(self):
        return ('Lives: {}'.format(self.lives))

class PowerLaunch():
    def __init__(self):
        self.mp3 = 'power2'
        self.check_busy = True

class PressedBin():
    def __init__(self, num):
        self.num = num

class PressedBinEval():
    def __init__(self, num, result):
        self.num = num
        self.result = result

class Score():
    def __init__(self, points):
        self.points = points
        self.string = 'Score is {}'.format(self.points)
        self.pause_gameplay = True

    def __repr__(self):
        return('Score: {}'.format(self.points))

class SpinnerCollide():
    def __init__(self):
        self.mp3 = 'spin'
        self.pause_gameplay = True

class TestNotes():
    def __init__(self):
        self.pause_gameplay = True

class TogglePause():
    def __init__(self):
        self.pause_gameplay = True

class TubeTravel():
    def __init__(self):
        self.mp3 = 'suck'
        self.pause_gameplay = True

class EventManager():
    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def post(self, event):
        for listener in self.listeners:
            listener.notify(event)
