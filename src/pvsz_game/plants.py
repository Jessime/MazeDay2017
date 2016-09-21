# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 23:26:44 2016

@author: jessime
"""

import time

class Plant():

    def __init__(self, pos, board, cost=50):
        self.pos = pos
        self.board = board
        self.cost = cost

        self.level = 1
        self.health = 100

    def alive(self):
        return self.health > 0

class Sun():

    gold = 50

    def __init__(self, pos, spawn_time):
        self.pos = pos
        self.lifetime = 20
        self.spawn_time = spawn_time
        self.collected = False

    def __str__(self):
        return 'Sun'

    def __repr__(self):
        return str(self)

    def alive(self):
        return (self.lifetime > (time.time() - self.spawn_time)) and (not self.collected)

class Sunflower(Plant):

    def __init__(self, pos, board):
        super().__init__(pos, board)
        self.reload_time = 25
        self.time_til_reload = 25
        self.suns = 0

    def __str__(self):
        return 'Sunflower'

    def __repr__(self):
        return str(self) # Advised against http://stackoverflow.com/questions/727761/python-str-and-lists

    def spawn(self, timedelta):
        self.time_til_reload -= timedelta
        if self.time_til_reload <= 0:
            new_sun = Sun(self.pos, time.time())
            self.board[self.pos].append(new_sun)
            self.board.items['suns'].append(new_sun)
            self.time_til_reload = self.reload_time

    def level_up(self):
        pass #Maybe later

class PeaShooter(Plant):

    def __init__(self, pos, board, cost=100):
        super().__init__(pos, board)
        self.reload_time = 25
        self.time_til_reload = 25

    def __str__(self):
        return 'Sunflower'

    def __repr__(self):
        return str(self)

    def spawn(self, timedelta):
        pass