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
        print('')
        for k, v in sorted(self.__dict__.items()):
            print('{}: {}'.format(k, v))
        print('')
            
            
class Pokedex():
    """A collection of Pokemon that can be used in battle"""
    
    def __init__(self):
        self.name = 'pd'
        self.pm = {'pm'+str(i): Pokemon('pm'+str(i)) for i in range(1,7)}
        self.active = random.choice([i for i in self.pm.values()])
        
    def all_stats(self):
        for p in self.pm.values():
            p.stats()
            
    def switch(self, name):
        """Change the currently active pokemon"""
        self.active = self.pm[name]
        print('\n{} is now active.'.format(self.active.name))
        
    def now(self):
        print('\nYour current active pokemon is {}.'.format(self.active.name))
        print('Its health is at {}HP.\n'.format(self.active.health))
        
class Battle():
    """A minigame between player and NPC monsters."""
    
    def __init__(self, pokedex1, pokedex2, items1=None, items2=None):
        self.pd = pokedex1
        self.monsters = pokedex2
        self.items1 = items1
        self.items2 = items2
        self.finished = False
        
    def attack(self, as_cmd=True):
        report = '\n{} does {} damage to {}, who now has {}HP.\n'
        if as_cmd:
            self.monsters.active.health -= self.pd.active.power
            if self.monsters.active.health < 0:
                self.monsters.active.heath = 0
            print(report.format(self.pd.active.name,
                                self.pd.active.power, 
                                self.monsters.active.name,
                                self.monsters.active.health))
        else:
            self.pd.active.health -= self.monsters.active.power
            if self.pd.active.health < 0:
                self.pd.active.health = 0
            print(report.format(self.monsters.active.name,
                                self.monsters.active.power,
                                self.pd.active.name,
                                self.pd.active.heath))
    
    def cycle(self):
        """Take turns on both sides"""