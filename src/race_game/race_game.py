import pygame
import os

#"/cygdrive/c/Program Files (x86)/eSpeak/command_line/espeak.exe"
#os.system('"C:\Program Files (x86)\eSpeak\command_line\espeak.exe" "hello world"')

import game_utils
import track

#os.system('espeak "welcome to the race game"')

#response = input("Welcome to the race game!\
#	Press enter to start the game")

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
#moving_engine = pygame.mixer.Sound('sounds/laser_sustained.wav')
stalled_engine = pygame.mixer.Sound('sounds/stalled_engine.wav')
#turn_alert = pygame.mixer.Sound('sounds/chime_shortened-1sec.wav')
left_alert = pygame.mixer.Sound('sounds/left_espeak.wav')
right_alert = pygame.mixer.Sound('sounds/right_espeak.wav')

wall_hit = pygame.mixer.Sound('sounds/loud_concrete_step.wav')
splash = pygame.mixer.Sound('sounds/splash-jumping-b_shortened-1sec.wav')
hit_sound = pygame.mixer.Sound('sounds/hit.wav')
enemy_sound = pygame.mixer.Sound('sounds/space_chase.wav')
shot_sound = pygame.mixer.Sound('sounds/laser_shot.wav')
no_lasers = pygame.mixer.Sound('sounds/no_lasers.wav')
got_laser = pygame.mixer.Sound('sounds/laser.wav')
#win_music = pygame.mixer.Sound('sounds/game_win.wav')
win_message = pygame.mixer.Sound('sounds/win_message.wav')
ship_warning_sound = pygame.mixer.Sound('sounds/ship_warning.wav')
intro_message = pygame.mixer.Sound('sounds/intro_message.wav')

# Set up channels for playing sound
start_channel = pygame.mixer.Channel(1)
stalled_channel = pygame.mixer.Channel(2)
stalled_channel.set_volume(0.5)
moving_channel = pygame.mixer.Channel(3)
moving_channel.set_volume(0.1)
#obsticle_alert_channel = pygame.mixer.Channel(4)
#obsticle_outcome_channel = pygame.mixer.Channel(5)
wall_hit_channel = pygame.mixer.Channel(6)
wall_hit_channel.set_volume(1)
enemy_channel = pygame.mixer.Channel(7)
enemy_channel.set_volume(1)

clock = pygame.time.Clock()
t = 0
enemy_t = 0
is_moving = 0
is_enemy_moving = 1

pos = 0
enemy_pos = -7
lives = 3
lasers = 3
ship_warning = 0
#boost = 0

track = track.make_track(15)

my_event_IDs = {\
"left_turn": 25,\
"right_turn": 26,\
"left_response": 27,\
"right_response": 28,\
"laser": 29\
}

rt_alert = 0
lt_alert = 0
rt_response = 0
lt_response = 0

	# Don't allow the car to move before the race has started
start_channel.play(intro_message)
while start_channel.get_busy():
#	response = input()
#	if response == "c":
#		break
	continue
start_channel.play(race_start,maxtime=2250)
stalled_channel.play(stalled_engine)
while start_channel.get_busy():
	continue

# Start the game loop
while True:
	if is_moving == 0 and not stalled_channel.get_busy():
		stalled_channel.play(stalled_engine)

	dt = clock.tick()

	if is_enemy_moving == 1:
		if enemy_t < 1000:
			enemy_t+=dt
		else:
			enemy_pos+=1.5
			enemy_t = 0

	if pos-enemy_pos <= 3:
		if not enemy_channel.get_busy():
			enemy_channel.play(enemy_sound)
		if ship_warning == 0:
			channel = pygame.mixer.find_channel()
			channel.play(ship_warning_sound)
			ship_warning = 1		

	if pos-enemy_pos > 4:
		ship_warning = 0
		if enemy_channel.get_busy():
			enemy_channel.stop()


	if enemy_pos >= pos:
		lives-=1
		enemy_pos-=7
		channel = pygame.mixer.find_channel()
		channel.play(hit_sound)
		enemy_channel.stop()
		moving_channel.stop()
		is_moving = 0

	if lives < 1:
		pos = 0
		enemy_pos = -5
		lives = 3
		lasers=3
		start_channel.play(race_start,maxtime=2250)

	if pos >= max(track.keys())+5:
		pos = 0
		is_moving = 0
		is_enemy_moving = 0
		pygame.mixer.pause()
		start_channel.play(win_message)
		while start_channel.get_busy() == True:
			continue
		pygame.quit()

	if is_moving == 1:
		if t < 1000:
			t+=dt
		else:
			pos+=1			
			t = 0
			if pos in track.keys():
				obsticle = track[pos]
				pygame.time.set_timer(my_event_IDs[obsticle],100)
				
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:  
				pygame.quit()
			# Holding down up arrow moves the car
			if event.key == pygame.K_UP:
				moving_channel.play(moving_engine,loops=-1)
				stalled_channel.stop()
				is_moving = 1

			if event.key == pygame.K_RIGHT:
				if rt_alert == 0:
					wall_hit_channel.play(wall_hit)
#					pos-=0.5
				else:
					channel = pygame.mixer.find_channel()
					channel.set_volume(0.15)
					channel.play(car_turn)
					rt_alert = 0
					rt_response = 1
					enemy_pos-=1.5
					
			if event.key == pygame.K_LEFT:
				if lt_alert == 0:
					wall_hit_channel.play(wall_hit)
#					pos-=0.5
				else:
					channel = pygame.mixer.find_channel()
					channel.set_volume(0.15)
					channel.play(car_turn)
					lt_alert = 0
					lt_response = 1
					enemy_pos-=1.5

			if event.key == pygame.K_SPACE:
				if lasers >= 1:
					start_channel.play(shot_sound)
					enemy_channel.stop()
					enemy_pos-=3
					lasers-=1
				else:
					start_channel.play(no_lasers)

#			if event.key == pygame.K_DOWN:
#				if boost == 0: boost = 1
#				if boost == 1: boost = 0

		if event.type == my_event_IDs["left_turn"]:
			lt_alert = 1
			channel = pygame.mixer.find_channel()
			channel.set_volume(1,0)
			channel.play(left_alert)
			pygame.time.set_timer(my_event_IDs["left_turn"],0)
			lt_response = 0
			pygame.time.set_timer(my_event_IDs["left_response"],1500)

		if event.type == my_event_IDs["right_turn"]:
			rt_alert = 1
#			right_turn_channel.play(turn_alert)
			channel = pygame.mixer.find_channel()
			channel.set_volume(0,1)
			channel.play(right_alert)
			pygame.time.set_timer(my_event_IDs["right_turn"],0)
			rt_response = 0
			pygame.time.set_timer(my_event_IDs["right_response"],1500)

		if event.type == my_event_IDs["left_response"]:
			if lt_response == 0:
				moving_channel.stop()
				is_moving = 0
				pos-=1
				channel = pygame.mixer.find_channel()
				channel.play(splash)
			pygame.time.set_timer(my_event_IDs["left_response"],0)

		if event.type == my_event_IDs["right_response"]:
			if rt_response == 0:
				moving_channel.stop()
				is_moving = 0
				pos-=1
				channel = pygame.mixer.find_channel()
				channel.play(splash)
			pygame.time.set_timer(my_event_IDs["right_response"],0)

		if event.type == my_event_IDs["laser"]:
			channel = pygame.mixer.find_channel()
			channel.set_volume(1)
			channel.play(got_laser)
			lasers+=1
			pygame.time.set_timer(my_event_IDs["laser"],0)

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				moving_channel.stop()
				stalled_channel.play(stalled_engine,loops=-1)
				is_moving = 0

