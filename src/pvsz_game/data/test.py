import pygame
from subprocess import Popen

#pygame.init()
pygame.mixer.init()
Popen('mpg123 zombie.mp3'.split())
#grass = pygame.mixer.music.load('~/Code/MazeDay2017/src/data/pvsz/zombie.mp3')
