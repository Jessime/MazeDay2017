# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 18:46:58 2016

@author: jessime
"""

TYPE_STATS = [{'name':'Basic',
               'health':100,
               'pause':1,
               'attack':10
               }
              ]

class Zombie():

    def __init__(self, level, pos, board):
        self.level = level
        self.pos = pos
        self.board = board

        self.name = TYPE_STATS[self.level]['name']
        self.health = TYPE_STATS[self.level]['health']
        self.pause = TYPE_STATS[self.level]['pause']
        self.attack = TYPE_STATS[self.level]['attack']

    def __str__(self):
        return '{}Zombie({})'.format(self.name, self.health)

    def __repr__(self):
        return str(self)

    def spawn(self):
        self.board[self.pos].append(self)
        self.board.items['zombies'].append(self)

    def do_attack(self):
        pass

    def move(self, timedelta):
        if self.pause <= 0:
            self.pause = TYPE_STATS[self.level]['pause']
            left_pos = [self.pos[0], self.pos[1] - 1]
            contains_plant = self.board.is_plant(left_pos)
            if not any(contains_plant):
                index = self.board[self.pos].index(self)
                del self.board[self.pos][index]
                self.board[[self.pos[0], self.pos[1] - 1]].append(self)
                self.pos[1] -= 1

        else:
            self.pause -= timedelta

    def alive(self):
        return self.health > 0

    def update(self, timedelta):
        self.move(timedelta)
        self.do_attack()
        return self.pos[1] == 0