# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 23:14:44 2016

@author: jessime
"""
import argparse
import random
import pygame


class Board():

    def __init__(self):
        self.board = [[None]*100]*5

    def __getitem__(self, pos):
        return self.board[pos[0]][pos[1]]

    def __setitem__(self, pos, value):
        self.board[pos[0]][pos[1]] = value

class Player():

    def __init__(self):
        self.pos = [0, 0]
        self.alive = True

class PvsZ():

    def __init__(self):

        self.level = 1
        self.board = Board()
        self.player = Player()

    def check_arrows(self, event):
        """Move player on board if arrow key has been pressed."""
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if self.player.pos[1] > 0:
                    self.player.pos[1] -= 1
            if event.key == pygame.K_RIGHT:
                if self.player.pos[1] < 99:
                    self.player.pos[1] += 5
            if event.key == pygame.K_UP:
                if self.player.pos[0] > 0:
                    self.player.pos[0] -= 1
            if event.key == pygame.K_DOWN:
                if self.player.pos[0] < 4:
                    self.player.pos[0] += 5

            print(self.player.pos)
            print(self.board[self.player.pos])

    def run_level(self):
        for i in range(500):
            row = random.randint(0, 4)
            col = random.randint(0, 99)
            val = random.randint(1, 100)
            self.board[row, col] = val
        over = False
        while not over:
            for event in pygame.event.get():
                self.check_arrows(event)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        pygame.quit()
                        over = True
                        self.player.alive = False

    def run(self):
        pygame.init()
        pygame.display.set_mode()
        while self.player.alive:
            self.run_level()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_lvls', default=5, type=int, help='The number of levels you want to play')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print information to help with debugging.')
    parser.add_argument('-po', '--print_only', action='store_true', help='Set if you do not want to use sound-based sentences')
    parser.add_argument('-ns', '--no_sentences', action='store_true', help='Set if you do not want the sentences printed to the console.')
    args = parser.parse_args()

    game = PvsZ()
    game.run()