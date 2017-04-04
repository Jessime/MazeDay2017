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
        self.seg_color = (0,0,0)

    def exit_game(self):
        pygame.display.quit()
        pygame.quit()
        self.show()

    def initialize(self):
        print(str(self.event))
        pygame.init()
        self.screen = pygame.display.set_mode([self.model.width, self.model.height])

    def draw_ball(self, particle):
        pygame.draw.circle(self.screen,
                           particle.color,
                           (int(particle.x), int(particle.y)),
                           particle.size,
                           particle.thickness)

    def draw_particle(self):
        for particle in self.model.particle_list:
            pygame.draw.circle(self.screen, particle.color,
                               (int(particle.x), int(particle.y)),
                               particle.size,
                               particle.thickness)

    def draw_seg(self):
        for seg in self.model.segment_list:
            pygame.draw.line(self.screen, self.seg_color,
                            [seg.a.x,seg.a.y],
                            [seg.b.x,seg.b.y],
                            seg.thickness)

    def render(self):
        self.draw_ball(self.model.ball)
        self.draw_particle()
        self.draw_seg()

    def loop_end(self):
        if not self.model.running:
            return
        self.screen.fill(self.background_color)
        self.render()
        pygame.display.flip()
        self.clock.tick(60)

    def show(self):
        print('\n', self.event, '\n')

class AudioView(View):
    def __init__(self, ev_manager, model):
        super().__init__(ev_manager, model)
        self.event_func_dict = {}
        
    def play(self, filename=None):
        """Play the event mp3.

        Paramters
        ---------
        filename : str
            If filename is past, the corresponding mp3 file will be played instead of self.event.mp3.
        """
        if filename is None:
            filename = self.event.mp3
        template = pkg_resources.resource_filename('pinball_game', 'data/{}.mp3'.format(filename))
        pygame.mixer.music.load(template)
        pygame.mixer.music.play()
