# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 16:19:18 2017

@author: sksuzuki
"""

import pygame
import random
import math

background_colour = (255,255,255)
(width, height) = (400, 400)
drag = 0.999
elasticity = 0.75
gravity = (math.pi, 0.002)

class Flipper():
    
    def __init__(self,x,y,side):
        self.x = x
        self.y = y
        self.side = side
        
        self.length = 100
        self.width = 10
        