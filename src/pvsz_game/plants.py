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

        self.health = 100

    def alive(self):
        return self.health > 0

    def base_produce(self, timedelta):
        zombie = None
        self.time_til_reload -= timedelta
        if self.time_til_reload <= 0:
            self.time_til_reload = self.reload_time
            bullet_pos = [self.pos[0], self.pos[1] + 1]
            while True:
                try:
                    is_zombie = self.board.is_zombie(bullet_pos)
                except IndexError:
                    break
                if any(is_zombie):
                    zombie = self.board[bullet_pos][is_zombie.index(True)]
                    zombie.health -= self.damage
                    break
                else:
                    if bullet_pos[1] == 99:
                        break
                    bullet_pos[1] += 1
        if zombie is not None:
            return zombie

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
        self.reload_time = 6
        self.time_til_reload = 6
        self.suns = 0

    def __str__(self):
        return 'Sunflower({})'.format(self.health)

    def __repr__(self):
        return str(self) # Advised against http://stackoverflow.com/questions/727761/python-str-and-lists

    def produce(self, timedelta):
        self.time_til_reload -= timedelta
        if self.time_til_reload <= 0:
            new_sun = Sun(self.pos, time.time())
            self.board[self.pos].append(new_sun)
            self.board.items['suns'].append(new_sun)
            self.time_til_reload = self.reload_time

class PeaShooter(Plant):

    def __init__(self, pos, board):
        super().__init__(pos, board, cost=100)
        self.reload_time = 2
        self.time_til_reload = 2
        self.damage = 10

    def __str__(self):
        return 'PeaShooter({})'.format(self.health)

    def __repr__(self):
        return str(self)

    def produce(self, timedelta):
        self.base_produce(timedelta)


class CherryBomb(Plant):

    def __init__(self, pos, board):
        super().__init__(pos, board, cost=150)
        self.damage = 100
        self.time_to_detonate = 2

    def __str__(self):
        return 'CherryBomb'

    def __repr__(self):
        return str(self)

    def explode(self, active_pos):
        try:
            is_zombie = self.board.is_zombie(active_pos)
        except IndexError:
            return
        square = self.board[active_pos]
        for item, iz in zip(square, is_zombie):
            if iz:
                item.health -= self.damage

    def produce(self, timedelta):
        self.time_to_detonate -= timedelta
        if self.time_to_detonate <= 0:
            self.health = 0
            row_changes = (-1, 0, 1)
            col_changes = range(-5, 6)
            for i in row_changes:
                for j in col_changes:
                    active_pos = [self.pos[0] + i, self.pos[1] + j]
                    self.explode(active_pos)

class WallNut(Plant):

    def __init__(self, pos, board):
        super().__init__(pos, board, cost=50)
        self.health = 1200

    def __str__(self):
        return 'WallNut({})'.format(self.health)

    def __repr__(self):
        return str(self)

    def produce(self):
        pass

class SnowPea(Plant):

    def __init__(self, pos, board):
        super().__init__(pos, board, cost=225)
        self.reload_time = 2
        self.time_til_reload = 2
        self.damage = 10

    def __str__(self):
        return 'SnowPea({})'.format(self.health)

    def __repr__(self):
        return str(self)

    def produce(self, timedelta):
        zombie = self.base_produce(timedelta)
        if zombie is not None:
            zombie.freeze()


