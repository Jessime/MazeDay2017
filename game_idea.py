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
from dialog import Dialog

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
    
    def __init__(self, debug=False):
        self.debug = debug
        self.interpreter = Interpreter(self.debug)
        self.dialog = Dialog()

        self.i = I()
        self.drone = Drone(self.debug)
        
    def evaluate(self, cmd):
        try:
            eval(cmd)
        except:
            error = traceback.format_exc()
            if not self.debug:
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
        self.dialog.say('pm_battle1')
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
        self.dialog.say('intro1')
        self.command()  
        self.dialog.say('cmd1', loc=self.i.loc)
        self.i.add = types.MethodType(add, self.i)
        self.command()
        if 'drone' in self.i.items:
            self.dialog.say('drone1')
            self.command()
        else:
            print('You did not put the drone in your bag.')

            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', help="Print information to help with debugging.")
    parser.add_argument('-b', '--battle', action='store_true', help='Jump straight into a battle.')
    args = parser.parse_args()
    
    app = App(args.debug)
    app.run(args.battle)