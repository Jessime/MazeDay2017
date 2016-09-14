# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

class LoopEnd():

    def __init__(self):
        self.name = 'LoopEnd'

class GrowPlant():

    def __init__(self, plant, pos):
        self.plant = plant
        self.pos = pos

    def __str__(self):
        return '{} planted at {}.'.format(self.plant, self.pos)

class MoveObject():

    def __init__(self, obj, direction, step):
        self.obj = obj
        self.direction = direction
        self.step = step

    def __str__(self):
        return '{}: {}'.format(self.obj.name, self.obj.pos)

class CheckBoard():
    def __init__(self): pass
    def __str__(self): return 'Board state check requested.'

class EventManager():

    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def post(self, event):
        for listener in self.listeners:
            listener.update(event)
