# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 13:11:54 2016

@author: jessime
"""

import pygame
from subprocess import Popen

pygame.mixer.pre_init(int(22050*1.5))
pygame.init()
#pygame.mixer.init(int(22050*1.5))
soundfile = '/home/jessime/Documents/sound_sentences/long/23/24123.mp3'
pygame.mixer.music.load(soundfile)
pygame.mixer.music.play()
#play = Popen(['mpg123', '-q', soundfile])
data = input('this is a test: ')
print(data)