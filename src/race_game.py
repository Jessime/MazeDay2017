import pygame

# Set up mixer.
# The third parameter is the number of channels:
# 1 for mono and 2 for stereo
pygame.mixer.pre_init(44100,-16,2, 2048)
pygame.init()
#pygame.display.set_caption('Right arrow: right speaker concrete footstep\nLeft arrow: left speaker concrete footstep\nUp arrow: middle grass footstep\nEscape: quit game')
size = [100,100]
screen = pygame.display.set_mode(size)

# Initialize the game sounds
race_start = pygame.mixer.Sound('sounds/race_start.wav')
car_turn = pygame.mixer.Sound('sounds/car_turn.wav')
moving_engine = pygame.mixer.Sound('sounds/moving_engine.wav')
stalled_engine = pygame.mixer.Sound('sounds/stalled_engine.wav')
turn_alert = pygame.mixer.Sound('sounds/chime.wav')

# Set up channels for playing sound
start_channel = pygame.mixer.Channel(1)
stalled_channel = pygame.mixer.Channel(2)
moving_channel = pygame.mixer.Channel(3)
car_turn_channel = pygame.mixer.Channel(4)
turn_alert_channel = pygame.mixer.Channel(5)

stalled_channel.play(stalled_engine,loops=-1)
start_channel.play(race_start,maxtime=2250)

# Set up a user-defined event to increment the car along the track
# one position every second while the space bar is held
my_event = pygame.event.Event(1)
# Keep track of position with a counter
count = 0

# Start the game loop
while True:
	# Don't allow the car to move before the race has started
	if start_channel.get_busy():
		continue
	for event in pygame.event.get():
		if event.type == 1:
			if count == 4:
				turn_channel.play(car_turn)
				count = 0
			else:
				count+=1
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:  
				pygame.quit()
			# Holding down space moves the car
			if event.key == pygame.K_SPACE:
				moving_channel.play(moving_engine,loops=-1)
				stalled_channel.stop()				
				pygame.time.set_timer(1,1000)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				moving_channel.stop()
				stalled_channel.play(stalled_engine,loops=-1)
