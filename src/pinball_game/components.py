import math
import pygame


class Particle:
    """ A circular object with a velocity, size and mass """

    def __init__(self, x, y, size, mass=1):
        self.x = x
        self.y = y
        self.size = 15
        self.color = (0, 0, 255)
        self.thickness = 0
        self.speed = 10
        self.angle = 8
        self.mass = mass
        self.drag = 1
        self.elasticity = 0.9
        self.gravity = (math.pi, 0.05)

    def move(self):
        self.angle, self.speed = self.addVectors(self.angle,
                                                 self.speed,
                                                 self.gravity[0],
                                                 self.gravity[1])
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
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

    def bounce(self, width, height):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

    def addVectors(self,angle1, length1, angle2, length2):
        """ Returns the sum of two vectors """

        x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y  = math.cos(angle1) * length1 + math.cos(angle2) * length2

        angle  = 0.5 * math.pi - math.atan2(y, x)
        length = math.hypot(x, y)

        return (angle, length)

class Flipper():

    def __init__(self,x1,y1,x2,y2,x_on, y_on):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.x_on = x_on
        self.y_on = y_on
        self.x_off = self.x2
        self.y_off = self.y2

        self.flip_up = False
        self.flip_down = False
        self.line = None
        self.flipper_size = 15

    def move(self):
        """change flipper end position while flipping"""
        self.x2 = self.x_on if self.x2 == self.x_off else self.x_off
        self.y2 = self.y_on if self.y2 == self.y_off else self.y_off


    def update(self):
        if self.flip_up:
            self.move()
            if self.x2 == self.x_on:
                self.flip_up = False
                self.flip_down = True
        elif self.flip_down:
            self.move()
            if self.x2 == self.x_off:
                self.flip_down = False
