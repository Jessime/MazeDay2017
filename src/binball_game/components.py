import math
import pygame
import time
from random import uniform

import collision
import events

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
    def __init__(self, a, b, value=0, noise='seg2'):
        self.a = Point(*a)
        self.b = Point(*b)
        self.angle = (math.atan2(self.b.x-self.a.x, self.b.y-self.a.y) + math.pi/2) % (2*math.pi)

        self.value = value
        self.noise = noise
        self.thickness = 10

    def __repr__(self):
        base = '{}({}\n{}\nAngle: {:.2f})\n'
        return base.format(self.__class__.__name__, self.a, self.b, self.angle)

class Particle:
    """ A circular object with a velocity, size and mass """

    def __init__(self, x, y, size, value=0, noise='jump'):
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
        self.gravity = (3/2*math.pi, 0.065)
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

                # if isinstance(seg,Flipper):
                #     if seg.flip_up or seg.flip_down:
                #         self.speed *= 2

    def particle_bounce(self, particle_list):
        """Check for collision with all particles. Update attributes appropriately.

        Parameters
        ----------
        segment_list : [Particle]
            All particles in the model
        """
        for particle in particle_list:
            collision_occurs = collision.ball_circle(self,particle)
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

class Tube(Particle):

    def __init__(self, x, y, size, value=65, noise='suck'):
        super().__init__(x, y, size, value=65, noise='suck')

        self.color = (0, 100, 200)
        

class Bin():
    reload_time = 3
    last_pressed = 0
    reloaded = True

    def __init__(self, num, rekt, color, noise):
        self.num = num
        self.rekt = rekt
        self.color = color
        self.noise = noise

        self.original_color = color

    def pressed_event(self, ball):
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
            ball.angle = uniform(.25,.75)*math.pi
            ball.y = self.rekt.top - 15

        return message

    def update(self):
        Bin.reloaded = time.time() >= Bin.reload_time + Bin.last_pressed
        if Bin.reloaded:
            self.color = self.original_color
        else:
            self.color = (255, 255, 255)

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

    def __init__(self, rekt, value=70, noise='spin'):
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
                print(self.color)
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

def init_components(width, height):
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

    ball = Particle(599-16,1000-15,15) # real
    components_dict['ball'] = ball

    bin_0 = Bin(0, pygame.Rect(150,912,40,48), (0, 255, 255), 'flipper')
    bin_1 = Bin(1, pygame.Rect(150+40,912,80,48), (0, 255, 0), 'flipper')
    bin_2 = Bin(2, pygame.Rect(290,912,80,48), (255, 0, 0), 'flipper')
    bin_3 = Bin(3, pygame.Rect(290+80,912,40,48), (255, 0, 255), 'flipper')
    components_dict['bin_list'] = [bin_0, bin_1, bin_2, bin_3]

    spin = [Spinner(pygame.Rect(482, 400, 25, 25)),
            Spinner(pygame.Rect(5, 275, 25, 25)),
            Spinner(pygame.Rect(88, 0, 25, 25))]
    components_dict['spinner_list'] = spin
    # flipper_left = Flipper(Point(150, 912),
    #                        Point(245, 960),
    #                        1.57)
    # flipper_right = Flipper(Point(410, 912),
    #                         Point(315, 960),
    #                         1.57, 'r')
    # components_dict['flipper_left'] = flipper_left
    # components_dict['flipper_right'] = flipper_right

    segment_data = [((width-1-40, height-1), (width-1-40,150)), #shooter line
                      ((width-1, 25), (width-1-25,0),1), #top right corner
                      ((75, 0), (0,100),10), #top left corner
                      ((width-1-40,837), (410,912)), #right funnel
                      ((0,837), (150,912)), #left funnel
                      ((260, 370), (310, 390),20), #Middle
                      ((60,825), (100,700)), #eft triangle pt1
                      ((55,824), (150,860)), #left triangle pt2
                      #((100,697), (145,865)), #left triangle pt3
                      #((415,865),(460,697)), #right triangle pt1
                      ((410,860), (width-100,820)), #right triangle pt2
                      ((width-1-141,700), (width-1-100,825)),#right triangle pt3
                      ((width-1-40, 250), (width-1-150, 450)), #right tunnel top
                      ((width-1-40, 325), (width-1-150, 550)), #right tunnel bottom
                      ((35, 275), (100, 400)), #left tunnel top
                      ((0, 300), (75, 440)), #left tunnel bottom
                      ((80, 0), (78, 25)), # small top tunnel left
                      ((120, 0), (122, 25)) # small top tunnel right
                     ]

    segment_list = [Segment(*d) for d in segment_data]
    #segment_list.append(flipper_left)
    #segment_list.append(flipper_right)
    components_dict['segment_list'] = segment_list

    particle_data = [(295, 355, 25,10), #2
                     (245, 285, 25,10), #1
                     (345, 270, 25,10), #3
                     (50, 520, 10,10),  #1
                     (100, 550, 10,10), #3
                     (55, 585, 10,10)   #2
                    ]
    particle_list = [Particle(*d) for d in particle_data]
    components_dict['particle_list'] = particle_list

    return components_dict

def cap(width):
    launch_cap = Segment((width-1-40,150),(width-1,125))
    return launch_cap