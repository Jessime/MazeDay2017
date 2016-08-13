# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 21:28:33 2016

@author: jessime
"""

import inspect
import types
import traceback
import argparse

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

def add(self, item):
    self.items[item.name] = item
    
def go(self, loc):
    self.loc = loc
    print('Your location is now {}.'.format(self.loc))
    
class I():
    
    def __init__(self):
        self.items = {}
        self.loc = 'home'
        
    def skills(self, verbose=True):
        methods = inspect.getmembers(self, predicate=inspect.ismethod)[1:]
        methods = [m[0] for m in methods]
        if verbose:
            for i in methods:
                print(i)
        return methods
            
    def bag(self):
        if self.items:
            for i in self.items.keys():
                print(i)
        else:
            print('Your bag is currently empty')
            
class Drone():
    
    def __init__(self):
        self.name = 'drone'
        self.pos = None

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
        if DEBUG:
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

class Interpreter():
    """"""
    def __init__(self):
        self.cmd = None
        
    def parse(self, cmd):
        try:
            start = (cmd[:2] == 'i.') or (cmd[:2] == 'd.')
            call = '(' in cmd and ')' in cmd
            if start and call:
                cmd = 'self.' + cmd
                error = None
            else:
                error = 'This syntax is incorrect:'
            if '(drone)' in cmd:
                cmd = cmd.replace('(drone)', '(self.d)')
        except:
            error = traceback.format_exc()
            if DEBUG:
                print('1. ', error)
            print('This syntax is incorrect...')
        return error, cmd 
    
    def error_message(self, cmd):
        print(cmd)
        print('This error message would eventually be customized.')
        
class App():
    
    def __init__(self):
        self.interpreter = Interpreter()
        self.i = I()
        self.d = Drone()
        
    def evaluate(self, cmd):
        try:
            eval(cmd)
        except:
            error = traceback.format_exc()
            if not DEBUG:
                error = error.split('\n')[-2]
            print(error)
        
    def command(self):
        while True:
            cmd = input('Command: ')
            if cmd == 'done':
                break
            error, cmd = self.interpreter.parse(cmd)
            if error is None:
                self.evaluate(cmd)
            else:
                print(error)
                self.interpreter.error_message(cmd)
            
    def run(self):
        intro = input('Would you like to read the intro? [y/n]: ')
        if intro == 'y':
            with open('intro.txt') as infile:
                for line in infile:
                    print(line)
        self.i.go = types.MethodType(go, self.i)

        print('')
        print('You just finish reading the intro. Where would you like to go?')
        print('You just got a new skill! You can go places. Use i.go(\'place\')')
        print('You can see all of your skills by \'i.skills()\'.')
        print('Similarly, you can see the items you have in your possession by \'i.bag()\'.')
        print('Type \'done\' to exit a command loop.')
        print('')
        self.command()  
        print('')
        print('Good job with your first command.')
        print('You are currently at {}.'.format(self.i.loc))
        print('What is that in the corner? It is a drone.')
        print('You just got a new skill! You can pick things up. Use i.add(thing)')
        print('')
        self.i.add = types.MethodType(add, self.i)
        self.command()
        if 'drone' in self.i.items:
            print('')
            #print('You can control the drone by starting your commands with \'drone.\'.')
            print('You can control the drone by starting your commands with \'d.\'.')            
            #print('For example, \'drone.start()\' will launch the drone into a maze.')
            print('For example, \'d.start()\' will launch the drone into a maze.')
            print('Control the drone with with .f(), .b(), .l(), .r()')
            print('Which correspond to forward, back, left, right')
            print('More powerful drones will be able to go up and down as well.')
            print('')
            self.command()
        else:
            print('You did not put the drone in your bag.')

            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", '--debug', action='store_true', help="Print information to help with debugging.")
    args = parser.parse_args()
    
    DEBUG = args.debug
    
    app = App()
    app.run()
