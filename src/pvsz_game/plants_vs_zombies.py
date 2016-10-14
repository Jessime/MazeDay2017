# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 23:14:44 2016

@author: jessime
"""
import random
import time

import pvsz_game.events as events
from .controller import Controller
from .view import BasicView, AudioView
from .plants import Plant, PeaShooter, Sunflower, Sun
from .zombies import Zombie

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
        return '\n\n'.join(['{}: {}'.format(i, row) for i, row in enumerate(self.board)])

    def is_plant(self, pos):
        plants = [issubclass(i.__class__, Plant) for i in self.board[pos[0]][pos[1]]]
        return plants

    def is_zombie(self, pos):
        zombies = [isinstance(i, Zombie) for i in self.board[pos[0]][pos[1]]]
        return zombies

    def first_zombie_col(self, row_num):
        """Return column number of first zombie in row.

        Parameters
        ----------
        row_num : int
            Index of row to search.

        Returns
        -------
        col_num : int
            Index of the first column containing a zombie."""
        row = self.board[row_num]
        for col_num, square in enumerate(row):
            if any(self.is_zombie([row_num, col_num])):
                return col_num

    def del_item(self, item):
        """Removes an item from it's 2D location on the board.

        Parameters
        ----------
        item : class instance
            The specific item to be removed"""
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
                    self.del_item(i)
            filtered_items[name] = filtered_ls
        self.items = filtered_items

class Player():

    def __init__(self):
        self.name = 'Player'
        self.pos = [0, 0]
        self.alive = True
        self.gold = 50

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
        self.zombie_deaths_needed = 10 * self.level
        self.zombie_spawn_delay = 1
        self.zombie_spawn_delay_range = (5, 10)
        self.board = Board()
        self.player = Player()
        self.plant_lookup = {'Sunflower': Sunflower,
                             'PeaShooter': PeaShooter}
        self.loop_start = time.time()
        self.loop_time = 0

        self.ev_manager.register(self)

    def check_plant_production(self):
        for plant in self.board.items['plants']:
            plant.produce(self.loop_time)

    def check_zombie_spawning(self):
        self.zombie_spawn_delay -= self.loop_time
        if self.zombie_spawn_delay <= 0:
            new_zombie_lvl = random.randint(0, self.level - 1)
            new_zombie = Zombie(new_zombie_lvl, [random.randint(0, 4), 99], self.board)
            new_zombie.spawn()
            self.zombie_spawn_delay = random.randint(*self.zombie_spawn_delay_range)

    def update_zombies(self):
        self.check_zombie_spawning()
        kill_player = [z.update(self.loop_time) for z in self.board.items['zombies']]
        if any(kill_player):
            self.player.alive = False
            self.ev_manager.post(events.DeathByZombie())

    def grow_plant(self, new_plant, event):
            self.board[event.pos].append(new_plant)
            self.board.items['plants'].append(new_plant)
            self.player.gold -= new_plant.cost
            ev = events.GrowPlant(event.plant, event.pos, self.player.gold)
            self.ev_manager.post(ev)

    def try_planting(self, event):
        new_plant = self.plant_lookup[event.plant](list(event.pos), self.board)
        board_pos_empty = self.board[event.pos] == []
        enough_gold = new_plant.cost <= self.player.gold
        if board_pos_empty and enough_gold:
            self.grow_plant(new_plant, event)
        elif not board_pos_empty:
            pass
        elif not enough_gold:
            pass

    def try_collecting(self, event):
        """If there is a Sun at a position, convert it to player gold."""
        sun_list = [i for i in self.board[event.pos] if isinstance(i, Sun)]
        if sun_list:
            sun_list[0].collected = True
            self.player.gold += Sun.gold
            self.ev_manager.post(events.SunCollected(self.player.gold))

    def exit_game(self):
        self.player.alive = False

    def notify(self, event):
        if isinstance(event, events.MoveObject):
            event.obj.move(event.direction, event.step)
        elif isinstance(event, events.TryPlanting):
            self.try_planting(event)
        elif isinstance(event, events.TryCollecting):
            self.try_collecting(event)
        elif isinstance(event, events.LoopEnd):
            self.loop_time = time.time() - self.loop_start
            self.loop_start = time.time()
        elif isinstance(event, events.UserQuit):
            self.exit_game()

    def update(self):
        self.check_plant_production()
        self.update_zombies()
        self.board.clean()

    def run(self):
        self.ev_manager.post(events.Init())
        while self.player.alive:
            self.update()
            self.ev_manager.post(events.LoopEnd())

class PvsZ():

    def __init__(self, print_only=False, no_printing=False):
        self.ev_manager = events.EventManager()
        self.model = Model(self.ev_manager)
        self.controller = Controller(self.ev_manager, self.model)
        if not no_printing:
            self.basic_view = BasicView(self.ev_manager, self.model)
        if not print_only:
            self.audio_view = AudioView(self.ev_manager, self.model)