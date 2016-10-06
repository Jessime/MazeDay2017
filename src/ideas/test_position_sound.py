import pygame

# Set up mixer.
# The thired parameter is the number of channels:
# 1 for mono and 2 for stereo
pygame.mixer.pre_init(44100,-16,2, 2048)
pygame.init()
pygame.display.set_caption('Right arrow: right speaker concrete footstep\nLeft arrow: left speaker concrete footstep\nUp arrow: middle grass footstep\nEscape: quit game')
size = [100,100]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Set up three channels for playing sound.

# Channel 1 will play from the left speaker
c1 = pygame.mixer.Channel(1)
c1.set_volume(1,0)

# Channel 2 will play in the middle
c2 = pygame.mixer.Channel(2)
c2.set_volume(1)

# Channel 3 will play from the right
c3 = pygame.mixer.Channel(3)
c3.set_volume(0,1)

# Load audio files
grass = pygame.mixer.Sound('grass_footstep.wav')
concrete_loud = pygame.mixer.Sound('loud_concrete_step.wav')

while True:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				# For some reason, I have to
				# reset the volume each time for
				# correct positioning to work.
				# Note, pressing the arrow key too fast
				# will temporarily redirect audio to the middle.
				# We need to incorporate code to
				# wait until a sound has completely finished playing
				# before allowing another sound to play.
				c1.set_volume(1,0)
				c1.queue(concrete_loud)
			if event.key == pygame.K_RIGHT:
				c3.set_volume(0,1)
				c3.play(concrete_loud)
			if event.key == pygame.K_UP:
				c2.play(grass)
			if event.key == pygame.K_ESCAPE:  
				pygame.quit()
