# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 11:50:12 2016

@author: jessime
"""

import random
import argparse
import traceback

from interpreter import Interpreter

TYPES = ['earth', 'fire', 'water', 'air']

class Pokemon():
    
    def __init__(self, name):
        self.name = name
        self.type = random.choice(TYPES)
        self.level = random.randint(1, 10)
        self.health = random.randint(1, 10)*self.level + random.randint(1, 10)
        self.power = int(random.randint(5, 20)*self.level**.5)
        self.speed = random.randint(1,5)*self.level**2
        
    def stats(self):
        for k, v in sorted(self.__dict__.items()):
            print('{}: {}'.format(k, v))
            

class App():
    
    def __init__(self):
        self.interpreter = Interpreter(DEBUG)
        self.monsters = [Pokemon('bad'+str(i)) for i in range(1,7)]
        self.pm = {'pm'+str(i): Pokemon('pm'+str(i)) for i in range(1,7)}
        
    def evaluate(self, cmd):
        try:
            eval(cmd)
        except:
            error = traceback.format_exc()
            if not DEBUG:
                error = error.split('\n')[-2]
            else:
                print('New command: '+cmd)
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
        self.command()
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", '--debug', action='store_true', help="Print information to help with debugging.")
    args = parser.parse_args()
    
    DEBUG = args.debug
    
    app = App()
    app.run()