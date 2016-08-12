# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 21:28:33 2016

@author: jessime
"""

import inspect
import types
import traceback

    
def add(self, item):
    self.items[item.name] = item
    
def go(self, loc):
    self.loc = loc
    print(self.loc)
    
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
        self.pos = [0, 0, 0]
     

def command(i, drone):
    while True:
        cmd = input('Command: ')
        if cmd == 'done':
            break
        try:
            start = cmd[:2] == 'i.'
            method = cmd.split('.')[1].split('(')[0] in i.skills(verbose=False)
            valid = start and method
            if valid:
                eval(cmd)
            else:
                print('That was not a valid command.')
        except:
            print('Error. That was not a valid command.')
            #print(traceback.format_exc())
          
def play_game():
    i = I()
    drone = Drone()
    intro = input('Would you like to read the intro? [y/n]: ')
    if intro == 'y':
        with open('intro.txt') as infile:
            for line in infile:
                print(line)
    print('')
    print('You just finish reading the intro. Where would you like to go?')
    print('You just got a new skill! You can go places. Use i.go(\'place\')')
    print('You can see all of your skills by \'i.skills()\'.')
    print('Similarly, you can see the items you have in your possession by \'i.bag()\'.')
    i.go = types.MethodType(go, i)
    print('Type \'done\' to exit a command loop.')
    command(i, drone)     
    print('Good job with your first command.')
    print('You are currently at {}.'.format(i.loc))
    print('What is that in the corner? It is a drone.')
    print('You just got a new skill! You can pick things up. Use i.add(\'thing\')')
    i.add = types.MethodType(add, i)
    command(i, drone)
            
if __name__ == '__main__':
    play_game()
