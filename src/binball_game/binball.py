# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 23:14:44 2016

@author: jessime
"""
import time
import os
import math

import events
import collision
from controller import Controller
from view import BasicView, AudioView
from components import Particle, Bin, init_components, cap

import argparse

class Model():
    def __init__(self, ev_manager):
        self.ev_manager = ev_manager

        self.player_score = 0
        self.player_lives = 3
        self.launch_power = 0
        self.islaunched = False
        self.successful_launch = False
        self.failed_launch = False

        self.paused = False
        self.running = True
        self.width = 600
        self.height = 1000

        components_dict = init_components(self.width, self.height)
        self.ball = components_dict['ball']
        # self.ball.x = 250
        # self.ball.y = 700
        # self.angle = 1.5*math.pi
        #self.ball.y = 200
        #self.ball.angle = 1.25*math.pi
        # self.ball.speed = 10
        self.segment_list = components_dict['segment_list']
        self.particle_list = components_dict['particle_list']
        # self.flipper_left = components_dict['flipper_left']
        # self.flipper_right = components_dict['flipper_right']
        self.bin_list = components_dict['bin_list']
        self.spinner_list = components_dict['spinner_list']
        self.tube_manager = components_dict['tube_manager']
        self.curver_list = components_dict['curver_list']
        self.coin_list = components_dict['coin_list']

        self.starter_segs_len = len(self.segment_list) #TODO hack. used to check if cap has been added to launcher.

        self.event = None
        self.ev_manager.register(self)

    # def flip(self):
    #     if self.event.side == 'l':
    #         self.flipper_left.flip_up = True
    #     elif self.event.side == 'r':
    #         self.flipper_right.flip_up = True

    def notify(self, event):
        self.event = event
        if isinstance(event, events.UserQuit):
            self.exit_game()
        # elif isinstance(event, events.Flip):
        #     self.flip()
        elif isinstance(event, events.TogglePause):
            self.toggle_pause()
        elif isinstance(event, events.PowerLaunch):
            self.power_launch()
        elif isinstance(event, events.Launch):
            self.launch()
        elif isinstance(event, events.PressedBin):
            message = self.bin_list[self.event.num].pressed_event(self.ball)
            self.ev_manager.post(message)

    def exit_game(self):
        self.running = False

    def toggle_pause(self):
        self.paused = not self.paused

    def ball_collisions(self):
        self.ball.move()
        self.ball.bounce(self.width,
                         self.height,
                         self.segment_list,
                         self.particle_list)
        if self.ball.collision_partner is not None:
            self.player_score += self.ball.collision_partner.value
            mp3 = self.ball.collision_partner.noise
            self.ev_manager.post(events.Collision(mp3))
            self.ball.collision_partner = None

    def power_launch(self):
        if not self.islaunched:
            self.launch_power += 1

    def launch(self):
        if not self.islaunched:
            self.ball.angle = .5*math.pi
            self.ball.speed = 1.5*self.launch_power**.5 + 1
            self.islaunched = True

    def in_play(self):
        """Make sure ball isn't in launcher"""
        return self.ball.x < self.width - 40 - 1

    def check_in_bins(self):
        for bin_ in self.bin_list:
            contact = collision.ball_rect(self.ball, bin_.rekt)
            if contact and not bin_.active:
                bin_.active = True
                self.ball.angle = 1.5*math.pi
                self.ball.speed = 0#1
                self.ev_manager.post(events.Collision(bin_.noise, True))

    def check_spinners(self):
        for spinner in self.spinner_list:
            contact = collision.ball_rect(self.ball, spinner.rekt)
            if contact and not spinner.spinning:
                self.player_score += spinner.value
                spinner.spinning = True
                self.ev_manager.post(events.SpinnerCollide())

    def check_tubes(self):
        did_collide, points = self.tube_manager.update(self.ball)
        self.player_score += points
        if did_collide:
            self.ev_manager.post(events.TubeTravel())

    def check_curvers(self):
        for curver in self.curver_list:
            contact = collision.ball_circle(self.ball, curver)
            if contact:
                self.player_score += curver.value
                self.ball.angle += curver.curve
                self.ev_manager.post(events.Collision(curver.noise))

    def check_coin(self):
        index = None
        for i, coin in enumerate(self.coin_list):
            # print(i)
            contact = collision.ball_circle(self.ball, coin)
            if contact:
                self.player_score += coin.value
                self.ev_manager.post(events.Collision(coin.noise))
                index = i
                del self.coin_list[i]
        # print(i)

    def check_dying(self):
        if self.ball.y > self.height - 30 and self.in_play():
            self.player_lives -= 1
            self.reset()
            self.ev_manager.post(events.LifeLost())
            self.ev_manager.post(events.Score(self.player_score))

    def check_gameover(self):
        if self.player_lives == 0:
            #TODO happy noises
            self.running = False

    def reset_bins(self):
        for bin_ in self.bin_list:
            bin_.active = False

    def reset(self):
        self.ball = Particle(599-16,1000-15,15)
        self.ball.speed = 0
        self.islaunched = False
        self.successful_launch = False
        self.failed_launch = False
        self.launch_power = 0
        self.reset_bins()
        if len(self.segment_list) > self.starter_segs_len: #TODO hack
            del self.segment_list[-1]


    def failure_to_launch(self):
        """Evaluate sucess of launch.

        If sucessful, cap the launch ramp with a seg; otherwise, reset the ball.
        """
        if not self.successful_launch and not self.failed_launch and self.islaunched:
            if self.ball.x < self.width-41:
                self.successful_launch = True
                self.segment_list.append(cap(self.width))
            elif 3/2*math.pi - 0.1 < self.ball.angle < 3/2*math.pi + 0.1:
                self.failed_launch = True
                self.ev_manager.post(events.FailedLaunch())
                self.reset()

    def update_bins_spinners(self):
        _ = [b.update(self.bin_list) for b in self.bin_list]
        _ = [s.update() for s in self.spinner_list]

    def update(self):
        '''Main game logic.'''
        self.failure_to_launch()
        self.ball_collisions()
        self.update_bins_spinners()
        self.check_in_bins()
        self.check_spinners()
        self.check_tubes()
        self.check_curvers()
        self.check_coin()
        self.check_dying()
        self.check_gameover()
        # input('waiting :')

    def run(self):
        self.ev_manager.post(events.Init())
        while self.running:
            self.update()
            self.ev_manager.post(events.LoopEnd())

class App():
    def __init__(self, sound=True, video=True):
        self.ev_manager = events.EventManager()
        self.model = Model(self.ev_manager)
        self.basic_view = BasicView(self.ev_manager, self.model, video)
        if sound:
            self.audio_view = AudioView(self.ev_manager, self.model)
        self.controller = Controller(self.ev_manager, self.model)

if __name__ == '__main__':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    parser = argparse.ArgumentParser()
    parser.add_argument('-ns', '--no_sound', action='store_false')
    parser.add_argument('-nv', '--no_video', action='store_false')
    args = parser.parse_args()
    app = App(sound=args.no_sound, video=args.no_video)
    app.model.run()
