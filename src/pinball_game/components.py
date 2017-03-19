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

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.angle = (math.atan2(b.x-a.x, b.y-a.y) + math.pi/2) % (2*math.pi)

class Particle:
    """ A circular object with a velocity, size and mass """

    def __init__(self, x, y, size, mass=1):
        self.x = x
        self.y = y
        self.pos = Point(x, y)
        self.size = 15
        self.color = (0, 0, 255)
        self.thickness = 0
        self.speed = 10
        self.angle = 4.75
        self.mass = mass
        self.drag = 1
        self.elasticity = 0.9
        self.gravity = (3/2*math.pi, .25)

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
                print(self.pos)
                self.angle = 2*seg.angle - self.angle

    def particle_bounce(self):
        pass

    def bounce(self, width, height, segment_list):
        self.wall_bounce(width, height)
        self.seg_bounce(segment_list)
        self.particle_bounce()

    def addVectors(self,angle1, length1, angle2, length2):
        """ Returns the sum of two vectors """

        x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y  = math.cos(angle1) * length1 + math.cos(angle2) * length2

        angle  = math.atan2(x, y) % (2*math.pi)
        length = math.hypot(x, y)

        return (angle, length)

class Flipper():

    def __init__(self, a, b, on):
        self.a = a
        self.b = b
        self.on = on

        self.angle = (math.atan2(b.x-a.x, b.y-a.y) + math.pi/2) % (2*math.pi)
        self.off = self.b
        self.flip_up = False
        self.flip_down = False
        self.thickness = 15

    def __repr__(self):
        base = 'Flipper({}\n{}\nAngle: {:.2f})\n'
        return base.format(self.a, self.b, self.angle)

    def move(self):
        """change flipper end position while flipping"""
        self.b.x = self.on.x if self.b.x == self.off.x else self.off.y
        self.b.y = self.on.y if self.b.y == self.off.y else self.off.y


    def update(self):
        if self.flip_up:
            self.move()
            if self.b.x == self.on.x:
                self.flip_up = False
                self.flip_down = True
        elif self.flip_down:
            self.move()
            if self.b.x == self.off.x:
                self.flip_down = False
