# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime

I don't know the best way to order these, so they're in alphabetical order.
When making a event similar to another event, it's best if their first words are the same.
"""

class CheckBoard():
    def __init__(self):
        self.pause_gameplay = True
    def __str__(self): return 'Board state check requested.'

class CheckPlayer():
    def __init__(self, pos, gold):
        base = 'Position is {}, {}.\nGold is {}.'
        self.string = base.format(pos[0], pos[1], gold)
        self.pause_gameplay = True
        
    def __str__(self):
        return self.string

class CheckInPos():
    pass

class DeathByZombie():
    def __init__(self): pass
    def __str__(self): return 'Oh no! You have been eaten by a zombie! Please try again for redemption.'

class GrowPlant():
    def __init__(self, plant_name, pos, funds, noise):
        self.plant_name = plant_name
        self.pos = pos
        self.funds = funds
        self.mp3 = noise

    def __str__(self):
        base = '{} planted at {}.\nRemaining Suns: {}'
        return base.format(self.plant_name, self.pos, self.funds)

class Init():
    def __init__(self): pass
    def __str__(self): return 'Starting app.'

class InitLevel():
    def __init__(self):
        self.mp3 = 'start'
        self.pause_gameplay = True

class LoopEnd():
    def __init__(self):
        self.name = 'LoopEnd'

class MoveHome():
    def __init__(self):
        self.mp3 = 'home'
    def __str__(self):
        return 'Home. Postion now [1, 1]'

class NoGold():
    def __init__(self):
        self.mp3 = 'no_gold'
    def __str__(self):
        return 'You do not have enough gold for this transaction.'

class PlayerMoves():

    def __init__(self, obj, direction, step):
        self.obj = obj
        self.direction = direction
        self.step = step
        self.mp3 = 'move'

    def __str__(self):
        return '{}: {}'.format(self.obj.name, self.obj.pos)

class SunCollected():
    def __init__(self, gold):
        self.gold = gold
        self.mp3 = 'coins2'
    def __str__(self):
        return 'Sun collected! Total gold: {}'.format(self.gold)

class TogglePause():
    def __init__(self):
        self.pause_gameplay = True

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

class Win():
    def __str__(self): return 'Awesome, you have survived the horde!! Nice job.'


class EventManager():

    def __init__(self):
        self.listeners = []

    def register(self, listener):
        self.listeners.append(listener)

    def post(self, event):
        for listener in self.listeners:
            listener.notify(event)
