# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 21:28:33 2016

@author: jessime
"""

import inspect
import types
import traceback
import argparse

from interpreter import Interpreter
from drone import Drone
from pokemon import Pokedex

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
        
class App():
    
    def __init__(self):
        self.interpreter = Interpreter(DEBUG)
        self.i = I()
        self.d = Drone(DEBUG)
        
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
    
    def battle(self):
        self.i.add = types.MethodType(add, self.i)
        self.i.add(Pokedex())
        self.monsters = Pokedex()
        print('You are about to enter a battle.')
        print('You can get infomation about your pokemon through the pokedex.')
        print('Do \'pd.all_stats()\' to get the stats of all pokemon.')
        print('It is a 6 vs. 6 battle. You can attack with any pokemon at any time.')
        self.command()
        
    def run(self, battle=False):
        if battle:
            self.battle()
            return
            
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
    parser.add_argument('-d', '--debug', action='store_true', help="Print information to help with debugging.")
    parser.add_argument('-b', '--battle', action='store_true', help='Jump straight into a battle.')
    args = parser.parse_args()
    
    DEBUG = args.debug
    
    app = App()
    app.run(args.battle)
