# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 21:28:33 2016

@author: jessime
"""

import inspect

class I():
    
    def __init__(self):
        self.bag = {}
        
    def abilities(self):
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        print(methods)
        
i = I()
i.abilities()