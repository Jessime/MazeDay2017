import math
import pygame
import time
from random import uniform, choice
from itertools import cycle

import binball_game.collision as collision
import binball_game.events as events

class Point():
    def __init__(self, x, y=None):
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)

    def ints(self):
        return (int(self.x), int(self.y))

    def dot(self, v):
        return self.x*v.x + self.y*v.y

    def __add__(self, v):
        return Point(self.x+v.x, self.y+v.y)

    def __sub__(self, v):
        return Point(self.x-v.x, self.y-v.y)

    def __mul__(self, v):
        try:
            return Point(self.x*v.x, self.y*v.y)
        except AttributeError:
            return Point(self.x*v, self.y*v)

    def __truediv__(self, v):
        try:
            return Point(self.x/v.x, self.y/v.y)
        except AttributeError:
            return Point(self.x/v, self.y/v)

    def __neg__(self):
        return Point(self.x, self.y) * Point(-1, -1)

    def __str__(self):
        return "Point({:.3f}, {:.3f})".format(self.x, self.y)
    def __repr__(self):
        return str(self)

class Segment():
    """Line segment with which ball can interact

    Parameters
    ----------
    a : tuple
        Location of beginning of segment
    b : tuple
        Location of ending of segment

    Attributes
    ----------
    angle : float
        angle of segment in radians, where a horizontal segment is 0 or pi
    """
    def __init__(self, a, b, value=0, noise='seg2', color=(0,0,0)):
        self.a = Point(*a)
        self.b = Point(*b)
        self.angle = (math.atan2(self.b.x-self.a.x, self.b.y-self.a.y) + math.pi/2) % (2*math.pi)

        self.value = value
        self.noise = noise
        self.color = color
        self.thickness = 10

    def __repr__(self):
        base = '{}({}\n{}\nAngle: {:.2f})\n'
        return base.format(self.__class__.__name__, self.a, self.b, self.angle)

class Platforms():
    """ """

    def __init__(self, start_pt1, start_pt2, noise='seg2'):
        self.seg_1 = Segment(start_pt1, (start_pt1[0]+50, start_pt1[1]))
        self.seg_2 = Segment(start_pt2,
                             (start_pt2[0]+50, start_pt2[1]),
                             color=(184, 199, 224))
        self.distance = 600-41-200-50
        range_ = range(start_pt1[0], start_pt1[0]+self.distance, 2)
        self.pos_gen = cycle((*range_, *range_[::-1]))

    def update(self):
        new_pos = next(self.pos_gen)
        self.seg_1.a.x = new_pos
        self.seg_1.b.x = new_pos + 50
        self.seg_2.a.x = new_pos
        self.seg_2.b.x = new_pos + 50

class Particle():
    """ A circular object with a velocity, size and mass """

    def __init__(self, x, y, size, value=0, noise='jump', bin_gravity=0.01):
        self.x = x
        self.y = y
        self.size = size
        self.noise = noise
        self.value = value

        self.pos = Point(x, y)
        self.color = (0, 0, 255)
        self.thickness = 0
        self.max_speed = 25
        self._speed = 0
        self.angle = math.pi/2
        self.mass = 1
        self.drag = 1#.998
        self.elasticity = 0.82
        self.original_gravity = (3/2*math.pi, 0.065)
        self.bin_gravity = (3/2*math.pi, bin_gravity)
        self.gravity = self.original_gravity
        self.score = 0
        self.collision_partner = None

    def __repr__(self):
        return 'Particle({})'.format(self.pos)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, val):
        """Limit speed so  ball can't pass through objects or move too fast"""
        #self._speed = min(.5*self.size-1, val)
        self._speed = min(self.max_speed, val)

    def move(self):
        self.angle, self.speed = self.addVectors(self.angle,
                                                 self.speed,
                                                 self.gravity[0],
                                                 self.gravity[1])
        self.x += math.cos(self.angle) * self.speed
        self.y -= math.sin(self.angle) * self.speed
        self.pos = Point(self.x, self.y)
        self.speed *= self.drag

    def wall_bounce(self, width, height):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = (math.pi - self.angle) % (2*math.pi)
            self.speed *= self.elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = (math.pi - self.angle) % (2*math.pi)
            self.speed *= self.elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = -self.angle % (2*math.pi)
            self.speed *= self.elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = - self.angle % (2*math.pi)
            self.speed *= self.elasticity

    def seg_bounce(self, segment_list):
        """Check for collision with all segments. Update attributes appropriately.

        Parameters
        ----------
        segment_list : [Segment]
            All segments in the model
        """
        for seg in segment_list:
            did_collide = collision.segment_particle(seg, self)
            if did_collide:
                self.collision_partner = seg
                self.angle = (2*seg.angle - self.angle) % (2*math.pi)
                self.speed *= self.elasticity

                while collision.segment_particle(seg, self):
                    self.x += math.cos(self.angle)
                    self.y -= math.sin(self.angle)
                    self.pos = Point(self.x, self.y)

    def particle_bounce(self, particle_list):
        """Check for collision with all particles. Update attributes appropriately.

        Parameters
        ----------
        segment_list : [Particle]
            All particles in the model
        """
        for particle in particle_list:
            collision_occurs = collision.ball_circle(self, particle, True)
            if collision_occurs:
                self.collision_partner = particle
                self.speed *= self.elasticity

    def bounce(self, width, height, segment_list, particle_list):
        self.wall_bounce(width, height)
        self.seg_bounce(segment_list)
        self.particle_bounce(particle_list)

    def addVectors(self,angle1, length1, angle2, length2):
        """ Returns the sum of two vectors """

        x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y  = math.cos(angle1) * length1 + math.cos(angle2) * length2

        angle  = math.atan2(x, y) % (2*math.pi)
        length = math.hypot(x, y)

        return (angle, length)

class Coin(Particle):
    """An circular object with a value """

    def __init__(self,x ,y ,size, value, noise='coins'):
        super().__init__(x, y, size, value=value, noise=noise)
        self.color = (255,215,0)

class Tube(Particle):

    def __init__(self, x, y, size, drop_spot, ejection_angle,
                 value=85, noise='suck'):
        super().__init__(x, y, size, value=value, noise=noise)
        self.drop_spot = drop_spot
        self.ejection_angle = ejection_angle

        self.color = (22, 153, 19)

class TubeManager():
    """Repsonsible for controlling and updating Tube components

    Notes
    -----
    This departs from the style of the rest of the components.
    Usually collision detection and updating is handled by the Model.
    Because the tubes are 'connected', this is a good opportunity to test this style.

    Parameters
    ----------
    tube_list

    """
    def __init__(self, tube_list):
        self.tube_list = tube_list

    def teleport_ball(self, ball, tube):
        """Eject the ball from the drop spot of a different tube

        Parameters
        ----------
        ball : Particle
            Player ball
        tube : Tube
            Tube with which the ball originally collided
        """
        other_tubes = [t for t in self.tube_list if t is not tube]
        new_tube = choice(other_tubes)
        ball.x, ball.y = new_tube.drop_spot
        ball.angle = new_tube.ejection_angle + uniform(-.05, .05)

    def update(self, ball):
        """Checks for ball collisions and updates state appropriately.

        Parameters
        ----------
        ball : Particle
            Player ball

        Returns
        -------
        did_collide : bool
            True if ball interacted with one of the tubes
        points : int
            Value of tube doing the transporting
        """
        points = 0
        for tube in self.tube_list:
            did_collide = collision.ball_circle(ball, tube)
            if did_collide:
                points = tube.value
                self.teleport_ball(ball, tube)
                break
        return did_collide, points

class Bin():
    reload_time = 3
    last_pressed = 0
    reloaded = True

    def __init__(self, num, rekt, color, noise):
        self.num = num
        self.rekt = rekt
        self.color = color
        self.noise = noise

        self.out_noise = 'flipper'
        self._active = False
        self.active_color = (0, 0, 0)
        self.locked_color = (255, 255, 255)
        self.original_color = color

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value
        if self.active:
            self.color = self.active_color
        else:
            self.color = self.original_color

    def pressed_event(self, ball):
        """Key press is only valid if the Bins are currently reloaded"""
        message = None
        if  Bin.reloaded:
            Bin.last_pressed = time.time()
            message = self.do_key_press(ball)
        else:
            message = events.PressedBinEval(self.num, False)
        return message

    def do_key_press(self, ball):
        message = events.PressedBinEval(self.num, True)
        if self.rekt.collidepoint(ball.x, ball.y):
            Bin.last_pressed = 0
            message = events.PressedBinEval(self.num, 'collide')
            ball.speed = ball.max_speed * .75
            frac_of_bin = ((ball.y-self.rekt.top)/self.rekt.height)
            ball.angle = (0.25 + frac_of_bin*0.5)*math.pi
            ball.gravity = ball.original_gravity
            ball.y = self.rekt.top - 15
            self.active = False

        return message

    def update(self, bin_list):
        """Change the color if reload state changes"""
        #TODO This can be cleaner.
        #Not sure how to do this with @property since Bin.reloaded is a class attribute
        old_state = Bin.reloaded
        Bin.reloaded = time.time() >= Bin.reload_time + Bin.last_pressed
        switched = old_state != Bin.reloaded
        if switched and Bin.reloaded:
            for bin_ in bin_list:
                bin_.color = bin_.original_color
        elif switched:
            for bin_ in bin_list:
                bin_.color = bin_.locked_color

class Spinner():
    """Component that spins and flashes when activated by ball.

    Spinners are found in tunnels and freeze the ball while they're spinning.

    Parameters
    ----------
    rekt : pygame.Rect
        Location of spinner
    value : int (default=70)
        Points scored if ball interacts with component
    noise : str (default=spin)
        Name of mp3 to play when spinning

    Attributes
    ----------
    original_color : (int)
        Color of rekt when not spinning
    color : (int)
        Current color of rekt. Flashes when activated
    spinning : bool
        True if spinner has collided with ball and is currently activate
    spin_counter : int
        Number of frames spent spinning
    spin_left : int
        Number of frames left to spin
    """

    def __init__(self, rekt, value=75, noise='spin'):
        self.rekt = rekt
        self.value = value
        self.noise = noise

        self.original_color = (50, 100, 150)
        self.color = self.original_color
        self.spinning = False
        self.spin_counter = 100
        self.spin_left = self.spin_counter

    def update(self):
        if self.spinning:
            self.spin_left -= 1
            if self.spin_left % 10 == 0:
                if self.color == self.original_color:
                    self.color = (150, 100, 50)
                else:
                    self.color = self.original_color
        if self.spin_left == 0:
            self.spin_left = 100
            self.spinning = False

class Flipper():
    """Creates left and right flippers the player controls to hit the ball

    Parameters
    ----------
    a : Point
        Location of the base of flipper
    b : Point
        Location of the rotation end of flipper
    on_angle : float
        radian angle of flipper at the top of rotation when user flippers
    side : str (default='l')
        Indicates if flipper is on left or right side of board

    Attributes
    ----------
    rot : int
        Makes flipper rotate clockwise (-1) or counter-clockwise (1)
    len : float
        Length of flipper
    angle : float
        Current angle of flipper.
    off_angle : float
        radian angle of flipper at the bottom of rotation when user flippers
    flip_up : bool
        Is True after user 'flips', until angle ~= on_angle
    flip_down : bool
        Is True after angle ~= on_angle, until angle ~= off_angle
    thickness : int
        Visual thinkness of line
    """
    def __init__(self, a, b, on_angle, side='l'):
        self.a = a
        self.b = b
        self.on_angle = on_angle

        self.rot = 1 if side == 'l' else -1
        self.len = math.hypot(self.b.x - self.a.x, self.b.y - self.a.y)
        self.angle = (math.atan2(a.x-b.x, a.y-b.y) + math.pi/2) % (2*math.pi)
        self.off_angle = self.angle
        self.flip_up = False
        self.flip_down = False
        self.thickness = 1
        self.value = 0
        self.noise = 'flipper'

    def move(self):
        """change flipper end position while flipping"""
        if self.flip_up:
            self.angle += (.09 * self.rot)
        elif self.flip_down:
            self.angle -= (.09 * self.rot)
        self.angle %= 2*math.pi
        self.b.x = self.a.x + math.cos(self.angle) * self.len
        self.b.y = self.a.y - math.sin(self.angle) * self.len

    def test_flip_limit():
        pass

    def update(self):
        """Check flipping state and adjust angle and state accordingly"""
        delta = .15
        if self.flip_up:
            self.move()
            if self.on_angle - delta <= self.angle <= self.on_angle + delta:
                self.flip_up = False
                self.flip_down = True
        elif self.flip_down:
            self.move()
            if self.off_angle - delta <= self.angle <= self.off_angle + delta:
                self.flip_down = False

class CurveBall(Particle):
    """Slowly increments the balls angle while in effect field

    """
    def __init__(self, x, y, size, curve=.075, value=2, noise='chimes'):
        super().__init__(x, y, size, value=value, noise=noise)
        self.curve = curve

        self.color = (142, 19, 214)

def init_coin_list(width, height):
    coin_list =  [
    #   Coin(width-20, 200,9,50), #test coin
    #   Coin(width-20, 600,9,50)  #test coin
                 Coin(80,810,9,25),  #lt.1
                 Coin(112,822,9,25), #lt.4
                 Coin(95,777,9,25),  #lt.2
                 Coin(110,740,9,25), #lt.3
                 Coin(144,835,9,25), #lt.6
                 Coin(125,790,9,25), #lt.5
                 Coin(width-41-80,810,9,25),  #lrt.1
                 Coin(width-41-112,822,9,25), #rt.4
                 Coin(width-41-95,777,9,25),  #rt.2
                 Coin(width-41-110,740,9,25), #rt.3
                 Coin(width-41-144,835,9,25), #rt.6
                 Coin(width-41-125,790,9,25), #rt.5
                 Coin(30,20,15,100),
                 Coin(540,323,12,100),
                 #around main curver
                 Coin(188,500,9,25),
                 Coin(312,500,9,25),
                 Coin(250,438,9,25),
                 Coin(250,562,9,25),
                 Coin(280,552,9,25),
                 Coin(302,530,9,25),
                 Coin(280,448,9,25),
                 Coin(302,470,9,25),
                 Coin(198,470,9,25),
                 Coin(198,530,9,25),
                 Coin(220,552,9,25),
                 Coin(220,448,9,25),
                 Coin(250,500,12,100) #middle coin curver
                 ]
    for c in range(110,490,38):
        coin_list.append(Coin(c,85,9,25))
    return coin_list

def init_launch_runway(width, height):
    return pygame.Rect(width-1-40,150,40,height-150)

def init_ball(bin_gravity):
    return Particle(599-16,1000-15,15,bin_gravity=bin_gravity)
    # return Particle(200, 50, 15,bin_gravity=bin_gravity) #testing platforms

def init_bin_list():
    bins = [Bin(0, pygame.Rect(150,912,40,48), (255, 0, 255), 'note1'),
            Bin(1, pygame.Rect(150+40,912,80,48), (0, 255, 0), 'note2'),
            Bin(2, pygame.Rect(290,912,80,48), (255, 0, 0), 'note3'),
            Bin(3, pygame.Rect(290+80,912,40,48), (0, 255, 255), 'note4')]
    return bins

def init_spinner_list():
    spin = [Spinner(pygame.Rect(482, 400, 25, 25)), #left
            Spinner(pygame.Rect(5, 275, 25, 25)), #top
            Spinner(pygame.Rect(88, 0, 25, 25))] #right
    return spin

def init_tube_list(width):
    tube_list = [Tube(17, 50, 7, (17, 20), .25*math.pi), #top left corner
                 Tube(width - 60, 425, 7, (width-75, 440), 1.4*math.pi), # middle right
                 Tube(140, 15, 7, (111, 35), 1.5*math.pi)]
    return tube_list

def init_curver_list():
    curver_list = [CurveBall(250, 500, 50),
                   CurveBall(525, 250, 25),
                   CurveBall(520, 200, 20),
                   CurveBall(490, 290, 20)]
    return curver_list

def init_platforms():
    return Platforms((100,100),(100,650))

def init_left_flipper():
    flipper_left = Flipper(Point(150, 912),
                           Point(245, 960),
                           1.57)
    return flipper_left

def init_right_flipper():
    flipper_right = Flipper(Point(410, 912),
                            Point(315, 960),
                            1.57, 'r')
    return flipper_right

def init_segment_list(width, height):
    segment_data = [((width-1-40, height-1), (width-1-40,150)), #shooter line
                      ((width-1, 25), (width-1-25,0),1), #top right corner
                      ((75, 0), (0,100),10), #top left corner
                      ((width-1-40,837), (410,912)), #right funnel
                      ((0,837), (150,912)), #left funnel
                      ((260, 370), (310, 390),20), #Middle
                      ((55,820), (100,700)), #left triangle pt1
                      ((55,820), (150,860)), #left triangle pt2
                      ((410,860), (width-100,820)), #right triangle pt2
                      ((width-1-141,700), (width-100,820)),#right triangle pt3
                      ((width-1-40, 250), (width-1-150, 450)), #right tunnel top
                      ((width-1-40, 325), (width-1-150, 550)), #right tunnel bottom
                      ((35, 275), (100, 400)), #left tunnel top
                      ((0, 300), (75, 440)), #left tunnel bottom
                      ((80, 0), (78, 25)), # small top tunnel left
                      ((120, 0), (122, 25)), # small top tunnel right
                     ]
    segment_list = [Segment(*d) for d in segment_data]
    return segment_list

def init_particle_list():
    particle_data = [(295, 355, 25,10), #2
                     (245, 285, 25,10), #1
                     (345, 270, 25,10), #3
                     (50, 520, 10,10),  #1
                     (100, 550, 10,10), #3
                     (55, 585, 10,10)   #2
                    ]
    particle_list = [Particle(*d) for d in particle_data]
    return particle_list

def cap(width):
    launch_cap = Segment((width-1-40,150),(width-1,125))
    return launch_cap

def init_components(width, height, bin_gravity):
    """Set all the pieces of the game board to their proper locations

    Parameters
    ----------
    width : int
        width of screen
    height : int
        height of screen

    Returns
    -------
    components_dict : dict
        wrapper around all different types of components
    """
    components_dict = {}
    components_dict['launch_runway'] = init_launch_runway(width,height)
    components_dict['ball'] = init_ball(bin_gravity)
    components_dict['bin_list'] = init_bin_list()
    components_dict['spinner_list'] = init_spinner_list()
    components_dict['tube_manager'] = TubeManager(init_tube_list(width))
    components_dict['curver_list'] = init_curver_list()
    components_dict['coin_list'] = init_coin_list(width,height)
    components_dict['platforms'] = init_platforms()
    components_dict['segment_list'] = init_segment_list(width,height)
    components_dict['particle_list'] = init_particle_list()
    return components_dict
