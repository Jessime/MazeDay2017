# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

import pygame
import pkg_resources

from gtts import gTTS
from time import sleep

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
    def __init__(self, ev_manager, model, video=True):
        super().__init__(ev_manager, model)
        self.video = video

        self.clock = pygame.time.Clock()
        self.event_func_dict = {'Init': self.initialize,
                                'LoopEnd': self.loop_end,
                                'Lives': self.show,
                                'Score': self.show,
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

    def draw_particle(self):
        for particle in (*self.model.particle_list,
                         *self.model.tube_manager.tube_list,
                         *self.model.curver_list,
                         self.model.ball):

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

    def draw_bins_spinners(self):
        for comp in (*self.model.bin_list, *self.model.spinner_list):
            pygame.draw.rect(self.screen, comp.color, comp.rekt)

    def render(self):
        self.draw_bins_spinners()
        self.draw_particle()
        self.draw_seg()

    def loop_end(self):
        if not self.model.running:
            return
        if self.video:
            self.screen.fill(self.background_color)
            self.render()
        pygame.display.flip()
        self.clock.tick(60)

    def show(self):
        print('\n', self.event, '\n')

class AudioView(View):
    def __init__(self, ev_manager, model):
        super().__init__(ev_manager, model)
        self.event_func_dict = {'Collision' : self.play,
                                'PressedBinEval' : self.eval_bin,
                                'Launch' : self.play,
                                'LifeLost' : self.play,
                                'Lives' : self.play,
                                'Score' : self.tts_and_play,
                                'PowerLaunch' : self.play,
                                'FailedLaunch' : self.play,
                                'SpinnerCollide' : self.play,
                                'TestNotes' : self. test_notes,
                                'TogglePause' : self.toggle_pause,
                                'TubeTravel' : self.play}

        self.bin_noise_dict = {True:'coins',
                               False:'error',
                               'collide':'flipper'}

    def test_notes(self):
        """Allows user to corresponding bins and key presses to proper notes."""
        keys = 'DFJK'
        for i, k in enumerate(keys):
            self.play('{}_test'.format(k))
            self.play('note{}'.format(i+1))

    def eval_bin(self):
        """Decide which noise to play for bin press."""
        self.play(self.bin_noise_dict[self.event.result])

    def toggle_pause(self):
        if self.model.paused:
            self.play('pause')
        else:
            self.play('resume')

    def skip_on_busy(self):
        """Decides if mp3 should play or not.

        Returns
        -------
        skip : bool
            If True, mp3 file will not play
        """
        skip = False
        try:
            check_busy = self.event.check_busy
        except AttributeError:
            check_busy = False
        if check_busy and pygame.mixer.music.get_busy():
            skip = True
        return skip

    def check_pause_gameplay(self):
        """Decide if game should be slept until mp3 is finished"""
        try:
            pause = self.event.pause_gameplay
        except AttributeError:
            pause = False
        if pause:
            while pygame.mixer.music.get_busy():
                sleep(.1)

    def play(self, filename=None):
        """Play the event mp3.

        Event can also contain keyword attributes:
        * check_busy - event mp3 will only play if no other noise is being played
        * pause_gameplay - event mp3 will play until finished before returning

        Parameters
        ---------
        filename : str
            If filename is past, the corresponding mp3 file will be played instead of self.event.mp3.
        """

        if filename is None:
            filename = self.event.mp3
        if filename == '': #TODO fix this
            return

        if self.skip_on_busy():
            return

        #template = pkg_resources.resource_filename('pinball_game', 'data/{}.mp3'.format(filename))
        template = 'data/{}.mp3'.format(filename)
        pygame.mixer.music.load(template)
        pygame.mixer.music.play()

        self.check_pause_gameplay()

    def tts_and_play(self):
        """Uses Google's text-to-speech to play an event's string"""
        gTTS(self.event.string).save('data/temp.mp3')
        self.play('temp')
