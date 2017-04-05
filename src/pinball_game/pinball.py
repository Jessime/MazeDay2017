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
from view import BasicView, AudioView
from components import init_components, Particle


class Model():
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager

        self.player_score = 0
        self.player_lives = 3
        self.islaunched = False

        self.loop_start = time.time()
        self.loop_time = 0
        self.running = True
        self.width = 600
        self.height = 1000

        components_dict = init_components(self.width, self.height)
        self.ball = components_dict['ball']
        self.segment_list = components_dict['segment_list']
        self.particle_list = components_dict['particle_list']
        self.flipper_left = components_dict['flipper_left']
        self.flipper_right = components_dict['flipper_right']

        self.event = None
        self.ev_manager.register(self)

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
        elif isinstance(event, events.PowerLaunch):
            self.launch()

    def update(self):
        '''All game logic.'''
        # self.flipper_left.update()
        # self.flipper_right.update()
        self.ball.move()
        self.ball.bounce(self.width, self.height, self.segment_list, self.particle_list)
        self.flipper_left.update()
        self.flipper_right.update()
        self.check_dying()
        self.check_gameover()

    def run(self):
        self.ev_manager.post(events.Init())
        while self.running:
            self.update()
            self.ev_manager.post(events.LoopEnd())

    def launch(self):
        self.ball.speed = self.event.power*.5  +1
        self.islaunched = True

    def check_dying(self):
        if self.ball.y > self.height - 30 and self.ball.x < self.width - 40 -1:
            self.player_lives -= 1
            self.reset()

    def check_gameover(self):
        if self.player_lives == 0:
            #TODO sad noises
            self.running = False

    def reset(self):
        self.ball = Particle(599-16,1000-15,15)
        self.speed = 0
        self.islaunched = False

class App():
    def __init__(self, sound=True, printing=True):
        self.ev_manager = events.EventManager()
        self.model = Model(self.ev_manager)
        self.controller = Controller(self.ev_manager, self.model)
        if sound:
            self.audio_view = AudioView(self.ev_manager, self.model)
        if printing:
            self.basic_view = BasicView(self.ev_manager, self.model)

if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    app = App()
    app.model.run()
