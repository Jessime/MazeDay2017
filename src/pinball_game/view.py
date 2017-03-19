# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

import pygame

class View:
    def __init__(self, ev_manager, model):
        self.ev_manager = ev_manager
        self.model = model

        self.event = None

        self.ev_manager.register(self)

    def notify(self, event):
        self.event = event
        name = event.__class__.__name__
        if name in self.event_func_dict:
            self.event_func_dict[name]()

class BasicView(View):
    def __init__(self, ev_manager, model):
        super().__init__(ev_manager, model)

        self.clock = pygame.time.Clock()
        self.event_func_dict = {'Init': self.initialize,
                                'LoopEnd': self.loop_end,
                                'UserQuit': self.exit_game}

        self.background_color = (255,255,255)
        self.screen = None
        self.flipper_color = (0,0,0)

    def exit_game(self):
        pygame.display.quit()
        pygame.quit()
        self.show()

    def initialize(self):
        print(str(self.event))
        pygame.init()
        self.screen = pygame.display.set_mode([self.model.width, self.model.height])

    def draw_particle(self, particle):
        pygame.draw.circle(self.screen,
                           particle.color,
                           (int(particle.x), int(particle.y)),
                           particle.size,
                           particle.thickness)

    def draw_flipper(self,flipper):
        pygame.draw.line(self.screen, self.flipper_color,
                        [flipper.a.x,flipper.a.y],
                        [flipper.b.x,flipper.b.y],
                        flipper.thickness)

    def render(self):
        self.draw_particle(self.model.ball)
        self.draw_flipper(self.model.flipper_left)
        self.draw_flipper(self.model.flipper_right)

    def loop_end(self):
        self.screen.fill(self.background_color)
        self.render()
        pygame.display.flip()
        self.clock.tick(60)

    def show(self):
        print('\n', self.event, '\n')
