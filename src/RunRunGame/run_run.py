#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 11:04:51 2016

@author: jessime
"""


import pygame
import time
from random import randint



class Car(object):
    def __init__(self):
        self.position = 'Center'
        self.distance = 0

def run():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    clock = pygame.time.Clock()
    FPS = 30

    #Initialize sounds
    #Initialize pictures
    car = Car()
    #This is for distance travelled. Once distance travelled equals the level distance, the level will finish.
    RACE_DISTANCE = randint(1000,2000)
    print(RACE_DISTANCE)

    racing = True
    start_time = time.time()
    current_time = start_time
    while racing:
        #Handling User input
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and car.position != "Right":
                    if car.position == "Center":
                        car.position = "Right"
                        #Play directional sound
                        print(car.position)
                    elif car.position =="Left":
                        car.position = "Center"
                        #Play directional sound
                        print(car.position)
                elif event.key == pygame.K_LEFT and car.position != "Left":
                    if car.position == "Center":
                        car.position = "Left"
                        print(car.position)
                    elif car.position == "Right":
                        car.position = "Center"
                        print(car.position)
                elif event.key == pygame.K_ESCAPE:
                    racing = False

        if car.distance == RACE_DISTANCE:
            break
        car.distance += 1
        clock.tick(FPS)
        current_time = time.time() - start_time
        print(int(current_time))
    pygame.quit()

if __name__ == '__main__':
    run()