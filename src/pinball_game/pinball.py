# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 23:14:44 2016

@author: jessime
"""
import time
import os
import math

import events
from controller import Controller
from view import BasicView
from components import Flipper, Particle, Segment, Point

class Model():
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager

        self.loop_start = time.time()
        self.loop_time = 0
        self.running = True
        self.width = 600
        self.height = 1000

        self.segment_list = []
        self.particle_list = []
        # self.ball = Particle(599-16,1000-16,15)
        self.ball = Particle(275,233,15) #gets stuck in x = 300-303
        self.ball.speed = 5
        self.ball.mass = 1

        self.flipper_left = Flipper(Point(125, 900),
                                    Point(210, 925),
                                    1.57)
        self.flipper_right = Flipper(Point(410, 900),
                                     Point(325, 925),
                                     1.57, 'r')

        self.event = None
        self.ev_manager.register(self)
        self.segment_list.append(self.flipper_left)
        self.segment_list.append(self.flipper_right)

        # shooter line
        self.segment_list.append(Segment(Point(self.width-1-40, self.height-1),
                                         Point(self.width-1-40,150)))
        # shooter angled line
        self.segment_list.append(Segment(Point(self.width-1, 25),
                                         Point(self.width-1-25,0)))

        self.segment_list.append(Segment(Point(75, 0),
                                         Point(0,100),1))

        self.segment_list.append(Segment(Point(0,863.2),
                                         Point(125,900)))

        self.particle_list.append(Particle(300, 333,30))

    def exit_game(self):
        self.running = False

    def flip(self):
        if self.event.side == 'l':
            self.flipper_left.flip_up = True
        elif self.event.side == 'r':
            self.flipper_right.flip_up = True

    def notify(self, event):
        self.event = event
        if isinstance(event, events.LoopEnd):
            self.loop_time = time.time() - self.loop_start
            self.loop_start = time.time()
        elif isinstance(event, events.UserQuit):
            self.exit_game()
        elif isinstance(event, events.Flip):
            self.flip()

    def update(self):
        '''All game logic.'''
        self.ball.move()
        self.ball.bounce(self.width, self.height, self.segment_list, self.particle_list)
        self.flipper_left.update()
        self.flipper_right.update()

    def run(self):
        self.ev_manager.post(events.Init())
        while self.running:
            self.update()
            self.ev_manager.post(events.LoopEnd())

class App():
    def __init__(self, print_only=False, no_printing=False):
        self.ev_manager = events.EventManager()
        self.model = Model(self.ev_manager)
        self.controller = Controller(self.ev_manager, self.model)
        self.basic_view = BasicView(self.ev_manager, self.model)

if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    app = App()
    app.model.run()
