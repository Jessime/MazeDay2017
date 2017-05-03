# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 23:14:44 2016

@author: jessime
"""
import time
import math

import binball_game.events as events
import binball_game.collision as collision
from .controller import Controller
from .view import BasicView, AudioView
from .components import Particle, Bin, init_components, cap, Coin, init_coin_list

class Model():
    """Handels logic for the system.

    Parameters
    ----------
    ev_manager : EventManager
        Coordinates message passing between MVC classes.
    difficulty : str (default='regular')
        Determines the reaction time necessary for successful hit out of a bin,
        controlled by changing the gravity in the bins.

    Attributes
    -------
    player_score : int
        Tally of points from ball interactions with components.
    score_multiplier : int
        Multipler for coin values after all coins have been collected and reset.
    player_lives : int
        Number of balls until game over.
    launch_power : int
        Determines how fast the ball will move which corresponds to how long the
        player holds down the spacebar. Low launch_powers will not successfully
        launch the ball into the main game board.
    islaunched : bool (default=False)
        Game play flag. Set to True once the player has let go of the spacebar.
    successful_launch : bool (default=False)
        Game play flag. Determines whether or not the ball has been successfully
        launched (is in the main playing field). A Segment will appear closing off
        the launching area.
    failed_launch : bool (default=False)
        Game option flag. If launch is unsuccessful (not enough launch_power),
        the ball is reset and player will be able to relaunch the ball.
    paused : bool (default=False)
        Game play flag. Option to pause game by freezing the frame.
    running : bool (default=True)
        Main loop flag. Game continues running until player wins/loses/quits.
    width : int
        Determines width of game board in pixels.
    height : int
        Determines height of game board in pixels.
    bin_gravity : {str : float}
        A dictionary mapping difficulty strings to gravity float values.
    ball : Particle
        A Particle that interacts with Components on the game board. The player can
        score points when the ball interacts with specific Components and can control
        the ball's trajectory after the ball falls into a bin. If the ball moves below
        the bin area, the player loses a life.
    segment_list : [Segment]
        A list of Segments that the ball will collide with.
    particle_list : [Particle]
        A list of Particle bumpers that the ball will collide with. Will add points to
        the player score when hit.
    launch_runway : Rect
        An invisible Rect that covers the area of the launching runway
    bin_list : [Bin]
        A list of Rects
    spinner_list : [Spinner]
        A list of Rects that change color once the ball interacts with one. Will add
        points to the player score when interacted with.
    tube_manager : TubeManager([Tube])
        Responsible for updating Tube components.
    curver_list : [CurveBall]
        A list of Particles that curves the ball's trajectory when the ball interacts with one.
        Will add points to the player score when interacted with.
    coin_list : [Coin]
        A list of Particles that adds points to the player score when interacted with. Once all
        coins have been collected, the coins will reset with an increased value.
    platforms : [Platforms]
        List of two Segments that move horizontally during game play. When the ball interacts
        with the upper Platform, the ball will teleport to the bottom Platform and fall down
        closer to the Bins.
    starter_segs_len : int
        Length of the original segment list which does not include the Segment blocking off
        the launch runway while the ball is in play in the main game board area.
    event :
        The last event received from ev_manager.
    """
    def __init__(self, ev_manager, difficulty):
        self.ev_manager = ev_manager
        self.difficulty = difficulty

        self.player_score = 0
        self.score_multiplier = 1
        self.player_lives = 3
        self.launch_power = 0
        self.islaunched = False
        self.successful_launch = False
        self.failed_launch = False

        self.paused = False
        self.running = True
        self.width = 600
        self.height = 1000

        difficulty_dict = {'veteran': 0.04,
                           'hard' : 0.02,
                           'regular': 0.01,
                           'easy': 0.005}
        self.bin_gravity = difficulty_dict[difficulty]
        components_dict = init_components(self.width, self.height, self.bin_gravity)
        self.ball = components_dict['ball']

        self.segment_list = components_dict['segment_list']
        self.particle_list = components_dict['particle_list']
        self.launch_runway = components_dict['launch_runway']
        self.bin_list = components_dict['bin_list']
        self.spinner_list = components_dict['spinner_list']
        self.tube_manager = components_dict['tube_manager']
        self.curver_list = components_dict['curver_list']
        self.coin_list = components_dict['coin_list']
        self.platforms = components_dict['platforms']

        self.starter_segs_len = len(self.segment_list) #TODO hack. used to check if cap has been added to launcher.

        self.start_coin_timer = None
        self.start_bin_timer = None
        self.current_coin_value = None

        self.ev_manager.register(self)
        self.event = None
        self.event_func_dict = {'UserQuit': self.exit_game,
                                'TogglePause': self.toggle_pause,
                                'PowerLaunch': self.power_launch,
                                'Launch': self.launch,
                                'PressedBin': self.pressed_bin,
                                'CheckCoinBonus': self.check_coin_bonus}

    def notify(self, event):
        self.event = event
        name = event.__class__.__name__
        if name in self.event_func_dict:
            self.event_func_dict[name]()

    def pressed_bin(self):
        bin_ = self.bin_list[self.event.num]
        message = bin_.pressed_event(self.ball)
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
                self.start_bin_timer = time.time()
                bin_.active = True
                self.ball.angle = 1.5*math.pi
                self.ball.speed = 0#1
                self.ball.gravity = self.ball.bin_gravity
                self.ev_manager.post(events.Collision(bin_.noise))

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

    def check_platforms(self):
        contact = collision.segment_particle(self.platforms.seg_1, self.ball)
        if contact:
            self.ball.x = self.platforms.seg_2.a.x
            self.ball.y = self.platforms.seg_2.a.y
            self.ball.angle = math.pi*1.5
            self.ball.speed = 0

    def check_coin_bonus(self):
        if self.event.time - self.start_coin_timer < 1:
            self.player_score += self.current_coin_value*2
            self.ev_manager.post(events.CoinBonus())

    def check_coin(self):
        index = None
        for i, coin in enumerate(self.coin_list):
            contact = collision.ball_circle(self.ball, coin)
            if contact:
                self.start_coin_timer = time.time()
                self.current_coin_value = coin.value
                self.player_score += coin.value*self.score_multiplier
                self.ev_manager.post(events.Collision(coin.noise))
                index = i
                del self.coin_list[i]
                if not self.coin_list:
                    self.score_multiplier += 1
                    self.coin_list = init_coin_list(self.width,self.height)

    def check_launcher_error(self):    # TODO hack
        if self.successful_launch:
            contact = collision.ball_rect(self.ball, self.launch_runway)
            if contact:
                self.ball.x = 200
                self.ball.y = 700
                self.ball.angle = math.pi*1.5
                self.ball.speed = 10

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
        self.ball = Particle(599-16,1000-15,15,self.bin_gravity)
        self.ball.speed = 0
        self.ball.gravity = self.ball.original_gravity
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
        self.check_platforms()
        self.platforms.update()
        self.check_in_bins()
        self.check_spinners()
        self.check_tubes()
        self.check_curvers()
        self.check_coin()
        self.check_launcher_error()
        self.check_dying()
        self.check_gameover()

    def run(self):
        self.ev_manager.post(events.Init())
        while self.running:
            self.update()
            self.ev_manager.post(events.LoopEnd())

class App():
    def __init__(self, sound=True, video=True, difficulty='regular'):
        self.ev_manager = events.EventManager()
        self.model = Model(self.ev_manager, difficulty)
        self.basic_view = BasicView(self.ev_manager, self.model, video)
        if sound:
            self.audio_view = AudioView(self.ev_manager, self.model)
        self.controller = Controller(self.ev_manager, self.model)
