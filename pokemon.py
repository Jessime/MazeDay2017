# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 11:50:12 2016

@author: jessime
"""

import random

TYPES = ['earth', 'fire', 'water', 'air']
NAMES = ['atrix', 'bane', 'cakks', 'devby', 'ever', 'freez', 'greef']
class Pokemon():
    
    def __init__(self, name):
        self.name = name
        self.type = random.choice(TYPES)
        self.level = random.randint(1, 10)
        self.health = random.randint(1, 10)*self.level + random.randint(1, 10)
        self.power = int(random.randint(5, 20)*self.level**.5)
        self.speed = random.randint(1,5)*self.level**2
        
    def stats(self):
        for k, v in sorted(self.__dict__.items()):
            print('{}: {}'.format(k, v))
            
class Pokedex():
    """A collection of Pokemon that can be used in battle"""
    
    def __init__(self):
        self.name = 'pd'
        self.pm = {'pm'+str(i): Pokemon('pm'+str(i)) for i in range(1,7)}
        
    def all_stats(self):
        for p in self.pm.values():
            p.stats()
            print('')