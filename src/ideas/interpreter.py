# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 11:31:37 2016

@author: jessime
"""

import traceback

class Interpreter():
    """"""
    def __init__(self, debug):
        self.cmd = None
        self.debug = debug
        self.keywords = {'enemy': 'self.battle.monsters.active.stats()',
                         'attack': 'self.battle.attack(True)'}
        
    def parse(self, cmd):
        self.cmd = cmd
        try:
            if cmd in self.keywords:
                return None, self.keywords[cmd]
                
            objects = ['i', 'd', 'pd'] + ['pm' + str(i) for i in range(1,7)]
            obj = cmd.split('.')[0]
            call = cmd.split('.')[1]
            
            start = obj in objects
            is_called = '(' in cmd and ')' in cmd
            if start and is_called:
                if obj == 'i':
                    cmd = 'self.'+ cmd
                elif cmd[:2] == 'pm':
                    cmd = 'self.i.items[\'pd\'].pm[\'{}\'].{}'.format(obj, call)
                else:
                    cmd = 'self.i.items[\'{}\'].{}'.format(obj, call)
                error = None
            else:
                if self.debug:
                    print(objects)
                    print(start)
                    print(is_called)
                error = 'This syntax is incorrect:'
            if '(drone)' in cmd:
                cmd = cmd.replace('(drone)', '(self.d)')
        except:
            error = traceback.format_exc()
            if self.debug:
                print('1. ', error)
            print('This syntax is incorrect...')
        return error, cmd 
    
    def error_message(self, cmd):
        print(cmd)
        print('This error message would eventually be customized.')