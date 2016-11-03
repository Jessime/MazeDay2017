# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:25:02 2016

@author: jessime
"""

import pygame
import pkg_resources

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
        self.event_func_dict = {'CheckBoard': self.check_board,
                                'CheckPlayer': self.check_player,
                                'DeathByZombie': self.show,
                                'GrowPlant': self.show,
                                'Init': self.initialize,
                                'LoopEnd': self.loop_end,
                                'MoveObject': self.move_object,
                                'SunCollected': self.show,
                                'UserQuit': self.exit_game,
                                'Win':self.show}

    def check_board(self):
        print('\n', self.model.board.items, '\n')
        print(self.model.board, '\n')

    def check_player(self):
        print('\n', 'Gold: {}'.format(self.model.player.gold), '\n')

    def exit_game(self):
        pygame.display.quit()
        pygame.quit()
        self.show()

    def initialize(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_mode([100, 100])

    def loop_end(self):
        self.clock.tick(20)

    def move_object(self):
        print(self.event)
        current_square = self.model.board[self.model.player.pos]
        print('Square contains: {}'.format(current_square))

    def show(self):
        print('\n', self.event, '\n')



class AudioView(View):

    def __init__(self, ev_manager, model):
        super().__init__(ev_manager, model)

        self.previous_player_row = None
        self.event_func_dict = {'CheckBoard': self.check_board,
                                'CheckPlayer': self.check_player,
                                'DeathByZombie': self.show,
                                'GrowPlant': self.show,
                                'LoopEnd': self.loop_end,
                                'MoveObject': self.move_object,
                                'SunCollected': self.show,
                                'UserQuit': self.show}

    def check_board(self): pass
    def check_player(self): pass
    def loop_end(self): pass
    def show(self): pass

    def move_object(self):
        row = self.model.player.pos[0]
        if row != self.previous_player_row:
            self.previous_player_row = row
            zombie_col = self.model.board.first_zombie_col(row)
            if zombie_col is not None:
                volume = (100 - zombie_col)/100
                pygame.mixer.music.set_volume(volume)
                self.play()

    def play(self):
        template = pkg_resources.resource_filename('pvsz_game', 'data/zombie.mp3')
        pygame.mixer.music.load(template)
        pygame.mixer.music.play()