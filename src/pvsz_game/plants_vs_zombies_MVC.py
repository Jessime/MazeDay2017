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
from plants import Sunflower

class Board():

    def __init__(self):
        self.items = {'plants' : [],
                      'suns' : [],
                      'zombies' : []}
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

    def remove_item(self, item):
        """Removes an item from it's 2D location on the board."""
        #print('Board: ', self.board[item.pos])
        #print('index: ', self.board[item.pos].index(item))
        index = self.board[item.pos[0]][item.pos[1]].index(item)
        del self.board[item.pos[0]][item.pos[1]][index]

    def clean(self):
        """Remove all objects that are no longer alive."""
        filtered_items = {}
        for name, ls in self.items.items():
            filtered_ls = []
            for i in ls:
                if i.alive():
                    filtered_ls.append(i)
                else:
                    self.remove_item(i)
            filtered_items[name] = filtered_ls
        self.items = filtered_items

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
        self.loop_start = time.time()
        self.loop_time = None

        self.ev_manager.register(self)

    def check_plant_spawning(self):
        for plant in self.board.items['plants']:
            plant.spawn(self.loop_time)

    def grow_plant(self, event):
        if self.board[event.pos] == []:
            new_plant = self.plant_lookup[event.plant](list(event.pos), self.board)
            self.board[event.pos].append(new_plant)
            self.board.items['plants'].append(new_plant)

    def update(self, event):
        if isinstance(event, events.MoveObject):
            event.obj.move(event.direction, event.step)
        elif isinstance(event, events.GrowPlant):
            self.grow_plant(event)
        elif isinstance(event, events.LoopEnd):
            self.loop_time = time.time() - self.loop_start
            self.loop_start = time.time()

    def run(self):
        while self.player.alive:
            self.check_plant_spawning()
            self.board.clean()
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