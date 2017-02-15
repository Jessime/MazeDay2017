import pygame

import game_utils

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
car_turn = pygame.mixer.Sound('sounds/car_turn_shortened-1sec.wav')
moving_engine = pygame.mixer.Sound('sounds/moving_engine.wav')
stalled_engine = pygame.mixer.Sound('sounds/stalled_engine.wav')
turn_alert = pygame.mixer.Sound('sounds/chime_shortened-1sec.wav')
wall_hit = pygame.mixer.Sound('sounds/loud_concrete_step.wav')
splash = pygame.mixer.Sound('sounds/splash-jumping-b_shortened-1sec.wav')

# Set up channels for playing sound
start_channel = pygame.mixer.Channel(1)
stalled_channel = pygame.mixer.Channel(2)
stalled_channel.set_volume(0.5)
moving_channel = pygame.mixer.Channel(3)
moving_channel.set_volume(0.3)
#obsticle_alert_channel = pygame.mixer.Channel(4)
#obsticle_outcome_channel = pygame.mixer.Channel(5)
wall_hit_channel = pygame.mixer.Channel(6)
wall_hit_channel.set_volume(1)

stalled_channel.play(stalled_engine,loops=-1)
start_channel.play(race_start,maxtime=2250)

# Set up a user-defined event to increment the car along the track
# one position every second while the space bar is held
#my_event = pygame.event.Event(25,name="turn")
# Keep track of position with a counter
#count = 0

clock = pygame.time.Clock()
t = 0
is_moving = 0

pos = 0

#track = {
#2: (obsticle_alert_channel,turn_alert,1,0),\
#4: (obsticle_alert_channel,car_turn,0,1),\
#6: (obsticle_alert_channel,turn_alert,0,1),\
#8: (obsticle_alert_channel,turn_alert,1,0)}

track = {\
2: "left_turn",\
4: "right_turn",\
6: "right_turn",\
8: "left_turn",\
}

my_event_IDs = {\
"left_turn": 25,\
"right_turn": 26,\
"left_response": 27,\
"right_response": 28\
}

rt_alert = 0
lt_alert = 0
rt_response = 0
lt_response = 0

# Start the game loop
while True:
	# Don't allow the car to move before the race has started
	if start_channel.get_busy():
		continue

	dt = clock.tick()
	if is_moving == 1:
		if t < 1000:
			t+=dt
		else:
			pos+=1			
			t = 0
			if pos in track.keys():
#				track[pos][0].play(track[pos][1])
				obsticle = track[pos]
				pygame.time.set_timer(my_event_IDs[obsticle],1000)
				
	for event in pygame.event.get():
#		print(event)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:  
				pygame.quit()
			# Holding down space moves the car
			if event.key == pygame.K_SPACE:
#				pygame.time.set_timer(25,1000)
				moving_channel.play(moving_engine,loops=-1)
				stalled_channel.stop()
				is_moving = 1

			if event.key == pygame.K_RIGHT:
				if rt_alert == 0:
					wall_hit_channel.play(wall_hit)
				else:
#					channel = pygame.mixer.find_channel()
#					channel.play(car_turn)
					rt_alert = 0
					rt_response = 1
					
			if event.key == pygame.K_LEFT:
				if lt_alert == 0:
					wall_hit_channel.play(wall_hit)
				else:
#					channel = pygame.mixer.find_channel()
#					channel.play(car_turn)
					lt_alert = 0
					lt_response = 1

#			if event.key == pygame.K_a:
#				pygame.time.set_timer(my_event_IDs["turn"],1000)

		if event.type == my_event_IDs["left_turn"]:
			lt_alert = 1
#			left_turn_channel.play(turn_alert)
			channel = pygame.mixer.find_channel()
			channel.set_volume(1,0)
			channel.play(turn_alert)
			pygame.time.set_timer(my_event_IDs["left_turn"],0)
			lt_response = 0
			pygame.time.set_timer(my_event_IDs["left_response"],1000)
		if event.type == my_event_IDs["right_turn"]:
			rt_alert = 1
#			right_turn_channel.play(turn_alert)
			channel = pygame.mixer.find_channel()
			channel.set_volume(0,1)
			channel.play(turn_alert)
			pygame.time.set_timer(my_event_IDs["right_turn"],0)
			rt_response = 0
			pygame.time.set_timer(my_event_IDs["right_response"],1000)

		if event.type == my_event_IDs["left_response"]:
			if lt_response == 0:
				pos-=2
				channel = pygame.mixer.find_channel()
				channel.play(splash)
			else:
				channel = pygame.mixer.find_channel()
				channel.set_volume(0.3)
				channel.play(car_turn)
			pygame.time.set_timer(my_event_IDs["left_response"],0)

		if event.type == my_event_IDs["right_response"]:
			if rt_response == 0:
				pos-=2
				channel = pygame.mixer.find_channel()
				channel.play(splash)
			else:
				channel = pygame.mixer.find_channel()
				channel.set_volume(0.3)
				channel.play(car_turn)
			pygame.time.set_timer(my_event_IDs["right_response"],0)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				moving_channel.stop()
				stalled_channel.play(stalled_engine,loops=-1)
				is_moving = 0
#		if event.type == 25:
#			game_utils.play_directional_sound(turn_alert,turn_alert_channel,0,1)
#			if count == 2:
#				turn_alert_channel.play(turn_alert)
#				game_utils.play_directional_sound(turn_alert,turn_alert_channel,0,1)
#				count+=1
#			elif count == 4:
#				game_utils.play_directional_sound(turn_alert,turn_alert_channel,1,0)
#				count = 0
#			else:
#				count+=1

