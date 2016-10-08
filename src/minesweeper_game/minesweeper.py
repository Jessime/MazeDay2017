# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 23:14:44 2016

@author: jessime
"""
import time
import random
import argparse

import events
from controller import Controller
from view import BasicView, AudioView


class Button():

    def __init__(self, board, pos):
        self.board = board
        self.pos = pos
        self.is_hidden = True
        self.is_flagged = False
        self.is_bomb = False
        self.number = None

    def get_neighbors(self):
        off_sets = [-1, 0, 1]
        checked = set()
        for i in off_sets:
            for j in off_sets:
                row = min(len(self.board) - 1, max(0, self.pos[0] + i))
                col = min(len(self.board) - 1, max(0, self.pos[1] + j))
                if (row, col) not in checked:
                    checked.add((row, col))
                    yield self.board[row][col]

    def calc_number(self):
        if self.is_bomb:
            return
        self.number = 0
        for neighbor in self.get_neighbors():
            self.number += neighbor.is_bomb

    def __str__(self):
        if self.is_flagged:
            return 'f'
        elif self.is_hidden:
            return ' '
        else:
            return str(self.number)

    def __repr__(self):
        return str(self)

class Model():

    def __init__(self, ev_manager, size=4, n_bombs=3):
        self.ev_manager = ev_manager
        self.size = 4
        self.n_bombs = 3
        assert 3 <= self.size <= 20, 'The size of the board must be between 3 and 20.'
        assert 1 <= self.n_bombs, 'You must have at least one bomb.'
        assert self.n_bombs <= (self.size**2 - 1), 'The number of bombs must be below {}'.format(self.n_bombs**2-1)
        self.loop_start = time.time()
        self.loop_time = 0
        self.board = []
        self.pos = [0, 0]
        self.running = True
        self.has_pressed = False
        self.event = None
        self.win = None
        self.event_func_dict = {'CountUnflagged' : self.count_unflagged,
                                'TryButtonPress': self.try_button_press,
                                'TryChangePos' : self.try_change_pos,
                                'TryFlagToggle' : self.try_flag_toggle,
                                'UserQuit': self.exit_game}

        self.ev_manager.register(self)


    def setup_board(self):
        button_flat_list = []
        for i in range(self.size):
            self.board.append([])
            for j in range(self.size):
                button = [i, j]
                self.board[-1].append(Button(self.board, button))
                button_flat_list.append(button)

        #Select bombs
        del button_flat_list[button_flat_list.index(self.event.pos)] #Remove pressed button
        bomb_pos_list = random.sample(button_flat_list, self.n_bombs)
        for pos in bomb_pos_list:
            self.board[pos[0]][pos[1]].is_bomb = True

        for i in range(self.size):
            for j in range(self.size):
                self.board[i][j].calc_number()

    def open_button(self, button):
        button.is_hidden = False
        if button.number == 0:
            for neighbor in button.get_neighbors():
                if neighbor.is_hidden:
                    self.open_button(neighbor)

    def count_unflagged(self):
        if self.has_pressed:
            flags = 0
            for row in self.board:
                for bomb in row:
                    flags += bomb.is_flagged
            self.ev_manager.post(events.FlagNum(self.n_bombs - flags))

    def try_button_press(self):
        if not self.has_pressed:
            self.has_pressed = True
            self.setup_board()
        button = self.board[self.pos[0]][self.pos[1]]
        if button.is_hidden and not button.is_flagged:
            self.open_button(button)
            if button.is_bomb:
                self.running = False
                self.ev_manager.post(events.Explode())
            else:
                self.ev_manager.post(events.ButtonPress(button))

    def try_change_pos(self):
        move = []
        if self.event.direction == 'up' and self.pos[0] - 1 >= 0:
            move = [0, -1]
        elif self.event.direction == 'down' and self.pos[0] + 1 <= (self.size - 1):
            move = [0, 1]
        elif self.event.direction == 'left' and self.pos[1] - 1 >= 0:
            move = [1, -1]
        elif self.event.direction == 'right' and self.pos[1] + 1 <= (self.size - 1):
            move = [1, 1]
        if move:
            self.pos[move[0]] += move[1]
            button = None
            if self.has_pressed:
                button = self.board[self.pos[0]][self.pos[1]]
            self.ev_manager.post(events.ChangePos(button))

    def try_flag_toggle(self):
        if self.has_pressed:
            button = self.board[self.event.pos[0]][self.event.pos[1]]
            if button.is_hidden:
                button.is_flagged = not button.is_flagged
                self.ev_manager.post(events.ToggleFlag())

    def exit_game(self):
        self.running = False

    def notify(self, event):
        self.event = event
        name = event.__class__.__name__
        if name in self.event_func_dict:
            self.event_func_dict[name]()

    def check_win(self):
        if self.has_pressed:
            for row in self.board:
                for button in row:
                    if button.is_bomb:
                        continue
                    elif button.is_hidden:
                        return
            else:
                self.win = True
                self.running = False

    def run(self):
        self.ev_manager.post(events.Init())
        while self.running:
            self.check_win()
            self.ev_manager.post(events.LoopEnd())
        if self.win:
            self.ev_manager.post(events.Win())

class App():

    def __init__(self, print_only=False, no_printing=False, size=4, n_bombs=3):
        self.ev_manager = events.EventManager()
        self.model = Model(self.ev_manager, size=size, n_bombs=n_bombs)
        self.controller = Controller(self.ev_manager, self.model)
        if not no_printing:
            self.basic_view = BasicView(self.ev_manager, self.model)
        if not print_only:
            self.audio_view = AudioView(self.ev_manager, self.model)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument('-v', '--verbose', action='store_true', help='Print information to help with debugging.')
    parser.add_argument('-s', '--size', default=4, type=int, help='Width and height of the board.')
    parser.add_argument('-n', '--n_bombs', default=3, type=int, help='Number of bombs to place on board.')
    parser.add_argument('-po', '--print_only', action='store_true', help='Set if you do not want to use sound-based sentences')
    parser.add_argument('-np', '--no_printing', action='store_true', help='Set if you do not want information printed to the console.')
    args = parser.parse_args()

    app = App(print_only=args.print_only,
              no_printing=args.no_printing,
              size=args.size,
              n_bombs=args.n_bombs)

    app.model.run()