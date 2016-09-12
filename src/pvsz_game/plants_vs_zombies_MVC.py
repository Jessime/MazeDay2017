# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 23:14:44 2016

@author: jessime
"""
import argparse
import random
import pygame
import time

import events
from controller import Controller
from view import BasicView

class Sunflower():

    def __init__(self):
        self.level = 1
        self.health = 100
        self.reload_time = 20
        self.time_til_spawn = 20
        self.suns = 0

    def __str__(self):
        return 'Sunflower'

    def __repr__(self):
        return str(self) # Advised against http://stackoverflow.com/questions/727761/python-str-and-lists

    def spawn_sun(self, timedelta):
        self.time_til_spawn -= timedelta
        if self.time_til_spawn <= 0:
            self.suns += self.level
            self.time_til_spawn = self.reload_time

    def level_up(self):
        pass #Maybe later

class Board():

    def __init__(self):
        self.board = []
        for i in range(5):
            self.board.append([])
            for i in range(100):
                self.board[-1].append([])

    def __getitem__(self, pos):
        return self.board[pos[0]][pos[1]]

    def __setitem__(self, pos, value):
        self.board[pos[0]][pos[1]] = value

    def __str__(self):
        return str(self.board)

class Player():

    def __init__(self):
        self.name = 'Player'
        self.pos = [0, 0]
        self.alive = True
        self.sun_points = 50

    def move(self, direction, step):
        if direction == 'up' and self.pos[0] - step >= 0:
            self.pos[0] -= step
        elif direction == 'down' and self.pos[0] + step <= 4:
            self.pos[0] += step
        elif direction == 'left' and self.pos[1] - step >= 0:
            self.pos[1] -= step
        elif direction == 'right' and self.pos[1] + step <= 99:
            self.pos[1] += step

class Model():

    def __init__(self, ev_manager):
        self.ev_manager = ev_manager

        self.level = 1
        self.board = Board()
        self.player = Player()

        self.plant_lookup = {'Sunflower': Sunflower}
        self.ev_manager.register(self)

    def update(self, event):
        if isinstance(event, events.MoveObject):
            event.obj.move(event.direction, event.step)
        if isinstance(event, events.GrowPlant):
            if self.board[event.pos] == []:
                print('pos: ', event.pos)
                print('square: ', self.board[event.pos])
                self.board[event.pos].append(self.plant_lookup[event.plant]())

#    def run_level(self):
#        over = False
#        while not over:
#            self.check_input()
#            self.update()
#            self.render()

    def run(self):
        while self.player.alive:
#            self.run_level()
            self.ev_manager.post(events.LoopEnd())

class PvsZ():

    def __init__(self):
        self.ev_manager = events.EventManager()
        self.model = Model(self.ev_manager)
        self.controller = Controller(self.ev_manager, self.model)
        self.basic_view = BasicView(self.ev_manager, self.model)

    def run(self):
        pygame.init()
        pygame.display.set_mode([100, 100])
        self.model.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_lvls', default=5, type=int, help='The number of levels you want to play')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print information to help with debugging.')
    parser.add_argument('-po', '--print_only', action='store_true', help='Set if you do not want to use sound-based sentences')
    parser.add_argument('-ns', '--no_sentences', action='store_true', help='Set if you do not want the sentences printed to the console.')
    args = parser.parse_args()

    game = PvsZ()
    game.run()