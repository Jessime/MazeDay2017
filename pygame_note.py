
from array import array
from time import sleep

import pygame
from pygame.mixer import Sound, get_init, pre_init

class Note(Sound):

    def __init__(self, frequency, volume=.1):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples

if __name__ == "__main__":
    pre_init(44100, -16, 1, 1024)
    pygame.init()
    pygame.display.set_mode()
    done = False
    while not done:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    n = Note(880).play(-1)
                    sleep(.5)
                    n.stop()
                if event.key == pygame.K_RIGHT:
                    n = Note(440).play(-1)
                    sleep(.5)
                    n.stop()
                if event.key == pygame.K_UP:
                    n = Note(220).play(-1)
                    sleep(.5)
                    n.stop()
                if event.key == pygame.K_DOWN:
                    n = Note(110).play(-1)
                    sleep(.5)
                    n.stop()
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    done = True