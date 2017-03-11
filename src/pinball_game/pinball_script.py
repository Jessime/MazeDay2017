import pygame
import random
import math

background_colour = (255,255,255)
(width, height) = (400, 800)
drag = 0.999
elasticity = 0.75
gravity = (math.pi, 0.02)
BLACK = (0,0,0)

def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

def addVectors(angle1, length1, angle2, length2):
    """ Returns the sum of two vectors """
    
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle  = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return (angle, length)

def combine(p1, p2):
    if math.hypot(p1.x - p2.x, p1.y - p2.y) < p1.size + p2.size:
        total_mass = p1.mass + p2.mass
        p1.x = (p1.x*p1.mass + p2.x*p2.mass)/total_mass
        p1.y = (p1.y*p1.mass + p2.y*p2.mass)/total_mass
        p1.angle, p1.speed = addVectors(p1.angle, p1.speed*p1.mass/total_mass, p2.angle, p2.speed*p2.mass/total_mass)
        p1.speed *= (p1.elasticity*p2.elasticity)
        p1.mass += p2.mass
        p1.collide_with = p2

def collide(p1, p2):
    """ Tests whether two particles overlap
        If they do, make them bounce, i.e. update their angle, speed and position """
    
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (p1.angle, p1.speed) = addVectors(p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass, angle, 2*p2.speed*p2.mass/total_mass)
        (p2.angle, p2.speed) = addVectors(p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass, angle+math.pi, 2*p1.speed*p1.mass/total_mass)
        elasticity = p1.elasticity * p2.elasticity
        p1.speed *= elasticity
        p2.speed *= elasticity

        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap



class Particle:
    """ A circular object with a velocity, size and mass """
    
    def __init__(self, x, y, size, mass=1):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = 1
        self.elasticity = 0.9

    def move(self):
        self.angle, self.speed = addVectors(self.angle, self.speed, gravity[0], gravity[1])
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag

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
        self.angle, self.speed = addVectors(self.angle, self.speed, *vector)
        
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

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity
    

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 8')


my_particles = []


size = 15 #random.randint(10, 20)
x = random.randint(size, width-size)
y = random.randint(size, height-size)

particle = Particle(x, y, size)
particle.speed = random.random()
particle.angle = random.uniform(0, math.pi*2)

my_particles.append(particle)

selected_particle = None
running = True

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
        self.update()
        
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
        self.line = pygame.draw.line(screen, BLACK, 
                                     [self.x1,self.y1],
                                     [self.x2,self.y2],
                                     15)
#        elif self.flip_down:
#            self


flipper_left = Flipper(100,700,150,730,100,650)
flipper_right = Flipper(350,700,300,730,350,650)

clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                flipper_left.flip_up = True
            elif event.key == pygame.K_j:
                flipper_right.flip_up = True
    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1

    screen.fill(background_colour)
#    pygame.draw.line(screen, BLACK, [100,700],[left_end_x,left_end_y],15)
#    pygame.draw.line(screen, BLACK, [350,700],[right_end_x,right_end_y],15)
        
    flipper_left.update()
    flipper_right.update()
    for i, particle in enumerate(my_particles):
        particle.move()
        particle.bounce()
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
        particle.display()

    pygame.display.flip()
    clock.tick(60)
