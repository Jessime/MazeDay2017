import math
import pygame

import collision

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
    a : Point
        Location of beginning of segment
    b : Point
        Location of ending of segment

    Attributes
    ----------
    angle : float
        angle of segment in radians, where a horizontal segment is 0 or pi
    """
    def __init__(self, a, b, value=0, noise=''):
        self.a = a
        self.b = b
        self.angle = (math.atan2(b.x-a.x, b.y-a.y) + math.pi/2) % (2*math.pi)

        self.value = value
        self.noise = noise
        self.thickness = 10

class Particle:
    """ A circular object with a velocity, size and mass """

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.pos = Point(x, y)
        self.size = size
        self.color = (0, 0, 255)
        self.thickness = 0
        self.speed = 1
        self.angle = math.pi/2
        self.mass = 1
        self.drag = 1
        self.elasticity = 0.9
        self.gravity = (3/2*math.pi, .25)
        self.score = 0

    def move(self):
        self.angle, self.speed = self.addVectors(self.angle,
                                                 self.speed,
                                                 self.gravity[0],
                                                 self.gravity[1])
        self.x += math.cos(self.angle) * self.speed
        self.y -= math.sin(self.angle) * self.speed
        self.pos = Point(self.x, self.y)
        self.speed *= self.drag

    def experienceDrag(self):
        self.speed *= self.drag

    def mouseMove(self, x, y):
        """ Change angle and speed to move towards a given point """

        dx = x - self.x
        dy = y - self.y
        self.angle = 0.5*math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1

    def accelerate(self, vector):
        """ Change angle and speed by a given vector """
        self.angle, self.speed = self.addVectors(self.angle, self.speed, *vector)

    def attract(self, other):
        """" Change velocity based on gravatational attraction between two particle"""

        dx = (self.x - other.x)
        dy = (self.y - other.y)
        dist  = math.hypot(dx, dy)

        if dist < self.size + self.size:
            return True

        theta = math.atan2(dy, dx)
        force = 0.2 * self.mass * other.mass / dist**2
        self.accelerate((theta- 0.5 * math.pi, force/self.mass))
        other.accelerate((theta+ 0.5 * math.pi, force/other.mass))

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
        for seg in segment_list:

            if collision.segment_particle(seg, self):
                self.score += seg.value
                self.angle = 2*seg.angle - self.angle
                if isinstance(seg,Flipper):
                    if seg.flip_up or seg.flip_down:
                        self.speed *= 2

    def particle_bounce(self, particle_list):
        for particle in particle_list:
            collision_occurs = collision.circle_circle(self, particle)
            if collision_occurs:
                break

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
        print(self.angle)
        self.off_angle = self.angle
        self.flip_up = False
        self.flip_down = False
        self.thickness = 1
        self.value = 0

    def __repr__(self):
        base = 'Flipper({}\n{}\nAngle: {:.2f})\n'
        return base.format(self.a, self.b, self.angle)

    def move(self):
        """change flipper end position while flipping"""
        if self.flip_up:
            self.angle += (.2 * self.rot)
        elif self.flip_down:
            self.angle -= (.2 * self.rot)
        self.angle %= 2*math.pi
        self.b.x = self.a.x + math.cos(self.angle) * self.len
        self.b.y = self.a.y - math.sin(self.angle) * self.len

    def test_flip_limit():
        pass

    def update(self):
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
