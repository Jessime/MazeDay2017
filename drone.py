# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 15:13:03 2016

@author: jessime
"""

maze = m = [[0,2,0,0,0,0,0,0,0],
            [0,1,0,1,1,1,0,0,0],
            [0,1,0,1,0,1,0,0,0],
            [0,1,0,1,0,1,0,0,0],
            [0,1,1,1,1,1,0,0,0],
            [0,1,0,1,0,0,0,0,0],
            [0,0,0,1,0,1,1,1,0],
            [0,0,0,1,0,1,0,1,0],
            [0,1,1,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,0]]
            
class Drone():
    
    def __init__(self, debug):
        self.name = 'd'
        self.pos = None
        self.debug = debug
        
    def start(self):
        self.pos = [9, 7]
        self.echo(9, 7)

    def move(self, row, col):
        if maze[row][col] == 1:
            self.pos = [row, col]
            self.echo(row, col)
        elif maze[row][col] == 2:
            print('Congrats, you finished!')
        else:
            print('There is a wall there.')
        if self.debug:
            print(self.pos)
            
    def f(self):
        row = self.pos[0] - 1
        col = self.pos[1]
        self.move(row, col)        

    def b(self):
        row = self.pos[0] + 1
        col = self.pos[1]
        self.move(row, col)    

    def l(self):
        row = self.pos[0]
        col = self.pos[1] - 1
        self.move(row, col)    

    def r(self):        
        row = self.pos[0]
        col = self.pos[1] + 1
        self.move(row, col)            

    def echo(self, row, col):
        up = maze[row - 1][col]
        down = maze[row + 1][col]
        left = maze[row][col - 1]
        right = maze[row][col + 1]
        print('_{}_'.format(up))
        print('{}_{}'.format(left, right))
        print('_{}_'.format(down))