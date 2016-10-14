# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime

I don't know the best way to order these, so they're in alphabetical order.
When making a event similar to another event, it's best if their first words are the same.
"""

class CheckBoard():
    def __init__(self): pass
    def __str__(self): return 'Board state check requested.'

class CheckPlayer():
    def __init__(self): pass
    def __str__(self): return 'Player state check requested.'

class DeathByZombie():
    def __init__(self): pass
    def __str__(self): return 'Oh no! You have been eaten by a zombie! Please try again for redemption.'

class GrowPlant():

    def __init__(self, plant, pos, funds):
        self.plant = plant
        self.pos = pos
        self.funds = funds

    def __str__(self):
        return '{} planted at {}.\nRemaining Suns: {}'.format(self.plant, self.pos, self.funds)

class Init():
    def __init__(self): pass
    def __str__(self): return 'Starting app.'

class LoopEnd():

    def __init__(self):
        self.name = 'LoopEnd'

class MoveHome():
    pass

class MoveObject():

    def __init__(self, obj, direction, step):
        self.obj = obj
        self.direction = direction
        self.step = step

    def __str__(self):
        return '{}: {}'.format(self.obj.name, self.obj.pos)

class SunCollected():

    def __init__(self, gold):
        self.gold = gold

    def __str__(self):
        return 'Sun collected! Total gold: {}'.format(self.gold)

class TryCollecting():

    def __init__(self, pos):
        self.pos = pos

    def __str__(self):
        return 'Trying to collect Sun at {}.'.format(self.pos)

class TryPlanting():

    def __init__(self, plant, pos):
        self.plant = plant
        self.pos = pos

    def __str__(self):
        return 'Trying to plant {} at {}.'.format(self.plant, self.pos)

class UserQuit():
    def __init__(self): pass
    def __str__(self): return 'Thanks for playing! We hope you enjoyed it.'


class EventManager():

    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def post(self, event):
        for listener in self.listeners:
            listener.notify(event)
