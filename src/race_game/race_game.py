import pygame
from pkg_resources import resource_filename

import race_game.track as track_maker
import race_game.aim as aim
import race_game.gameUtils as gameUtils
	
def run():

	base = resource_filename('race_game', 'sounds/{}.wav')
	
	# Set up mixer.
	# The third parameter is the number of channels:
	# 1 for mono and 2 for stereo
	pygame.mixer.pre_init(44100,-16,2, 2048)
	pygame.init()
	size = [100,100]
	screen = pygame.display.set_mode(size)
	
	# Initialize the game sounds
	race_start = pygame.mixer.Sound(base.format('race_start'))
	car_turn = pygame.mixer.Sound(base.format('car_turn_shortened-1sec'))
	moving_engine = pygame.mixer.Sound(base.format('moving_engine'))
	stalled_engine = pygame.mixer.Sound(base.format('stalled_engine'))
	left_alert = pygame.mixer.Sound(base.format('left_espeak'))
	right_alert = pygame.mixer.Sound(base.format('right_espeak'))
	wall_hit = pygame.mixer.Sound(base.format('loud_concrete_step'))
	splash = pygame.mixer.Sound(base.format('splash-jumping-b_shortened-1sec'))
	hit_sound = pygame.mixer.Sound(base.format('hit'))
	enemy_sound = pygame.mixer.Sound(base.format('space_chase'))
	shot_sound = pygame.mixer.Sound(base.format('laser_shot'))
	no_lasers = pygame.mixer.Sound(base.format('no_lasers'))
	got_laser = pygame.mixer.Sound(base.format('laser'))
	win_message = pygame.mixer.Sound(base.format('win_message'))
	ship_warning_sound = pygame.mixer.Sound(base.format('ship_warning'))
	intro_message = pygame.mixer.Sound(base.format('intro_message'))
	lost_life2 = pygame.mixer.Sound(base.format('lost_life_2left'))
	lost_life1 = pygame.mixer.Sound(base.format('lost_life_1left'))
	game_over = pygame.mixer.Sound(base.format('game_over'))
	missed_shot = pygame.mixer.Sound(base.format('missed_shot'))
	fire_laser = pygame.mixer.Sound(base.format('fire_laser'))
	ship_far = pygame.mixer.Sound(base.format('ship_far'))
	up = pygame.mixer.Sound(base.format("up_espeak"))
	down = pygame.mixer.Sound(base.format("down_espeak"))
	one = pygame.mixer.Sound(base.format("one_espeak"))
	two = pygame.mixer.Sound(base.format("two_espeak"))
	three = pygame.mixer.Sound(base.format("three_espeak"))
	aim_prefix = pygame.mixer.Sound(base.format('aim_prefix'))
	explode = pygame.mixer.Sound(base.format('medium_explosion'))
		
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
	
	track = track_maker.make_track(15)
	
	my_event_IDs = {\
	"left_turn": 25,\
	"right_turn": 26,\
	"left_response": 27,\
	"right_response": 28,\
	"laser": 29,\
	"aim_response": 30\
	}
	
	rt_alert = 0
	lt_alert = 0
	rt_response = 0
	lt_response = 0
	skip_intro = 0
	aiming = 0
	ship_close = 0
	aim_success = 0
	
	aim_dict = {\
		"left": left_alert,\
		"right": right_alert,\
		"up": up,\
		"down": down,\
		1: one,\
		2: two,\
		3: three}
	
	ship_aim_pos,aim_message = aim.aim_message()
	aim_pos = [0,0]
	aim_alert = 0
	shot_success = 0
	aimed = 0
	fire_alert = 0
	
	start_channel.play(intro_message)
	while start_channel.get_busy():
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					start_channel.stop()
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					break
		continue
	
	start_channel.play(race_start,maxtime=2250)
	stalled_channel.play(stalled_engine)
	while start_channel.get_busy():
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					break
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
	
		if pos-enemy_pos <= 4:
			ship_close = 1
			if aiming == 1:
				is_enemy_moving = 0
	
		if pos-enemy_pos <= 3:
			if not enemy_channel.get_busy():
				enemy_channel.play(enemy_sound)
			if ship_warning == 0 and aiming == 0:
				channel = pygame.mixer.find_channel()
				channel.play(ship_warning_sound)
				ship_warning = 1		
	
		if ship_close == 1 and aiming == 1:
			if pos-enemy_pos <= 1.5:
				break
			if aim_alert == 0:
				while start_channel.get_busy():
					continue
				gameUtils.play_single_sound(wall_hit_channel,aim_prefix)
				for sound in aim_message:
					gameUtils.play_single_sound(wall_hit_channel,aim_dict[sound])
				pygame.event.clear()
				pygame.time.set_timer(my_event_IDs["aim_response"],5000)	
				aim_alert = 1
	
		if aim_pos == ship_aim_pos:
			if fire_alert ==0:
				gameUtils.play_single_sound(start_channel,fire_laser)
				fire_alert = 1
			aimed = 1
	
		if pos-enemy_pos > 5:
			ship_warning = 0
			ship_close = 0
			if enemy_channel.get_busy():
				enemy_channel.stop()
			aim_alert = 0
	
		if enemy_pos >= pos:
			lives-=1
			enemy_pos-=7
			channel = pygame.mixer.find_channel()
			channel.play(hit_sound)
			enemy_channel.stop()
			moving_channel.stop()
			is_moving = 0
			if lives == 2:
				channel = pygame.mixer.find_channel()
				channel.play(lost_life2)
				while channel.get_busy():
					continue
			if lives == 1:
				channel = pygame.mixer.find_channel()
				channel.play(lost_life1)
				while channel.get_busy():
					continue
			if lives < 1:
				pygame.mixer.stop()
				channel = pygame.mixer.find_channel()
				channel.play(game_over)
				while channel.get_busy():
					continue			
				pygame.quit()
	#			pos = 0
	#			enemy_pos = -5
	#			lives = 3
	#			lasers=3
	#			start_channel.play(race_start,maxtime=2250)
	
		if pos >= max(track.keys())+5:
			pos = 0
			is_moving = 0
			is_enemy_moving = 0
			pygame.mixer.pause()
			start_channel.play(win_message)
			while start_channel.get_busy():
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
					if aiming == 1:
						aim_pos[1]+=1
	#					gameUtils.play_single_sound(wall_hit_channel,laser_aim)
						break
					moving_channel.play(moving_engine,loops=-1)
					stalled_channel.stop()
					is_moving = 1
	
				if event.key == pygame.K_RIGHT:
					if aiming == 1:
						aim_pos[0]+=1
	#					gameUtils.play_single_sound(wall_hit_channel,laser_aim)
						break
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
					if aiming == 1:
						aim_pos[0]-=1
	#					gameUtils.play_single_sound(wall_hit_channel,laser_aim)
						break
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
	
				if event.key == pygame.K_DOWN:
					if aiming == 1:
						aim_pos[1]-=1
	#					gameUtils.play_single_sound(wall_hit_channel,laser_aim)
						break
					if rt_alert == 1 or lt_alert == 1:
						break
					if moving_channel.get_busy():
						moving_channel.stop()
						is_moving = 0
					if pos-enemy_pos <= 2:
						break
					if lasers < 1:
						start_channel.play(no_lasers)
						break
					if ship_close == 0:
						start_channel.play(ship_far)
					aiming = 1
	
				if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
					if aiming == 1:
						aiming = 0
						aim_pos = [0,0]
	
				if event.key == pygame.K_SPACE:
					if aiming == 0:
						break
					if aiming == 1:
						pygame.time.set_timer(my_event_IDs["aim_response"],0)
						if aim_pos != ship_aim_pos:
							gameUtils.play_single_sound(wall_hit_channel,shot_sound)
							gameUtils.play_single_sound(wall_hit_channel,missed_shot)
							aiming = 0
							aim_pos = [0,0]
							lasers-=1
	#					if aim_pos == ship_aim_pos:
						if aimed == 1:
							enemy_channel.stop()
							gameUtils.play_single_sound(wall_hit_channel,shot_sound)
							channel = pygame.mixer.find_channel()
							channel.set_volume(0.1)
							channel.play(explode)
							enemy_pos-=5
							lasers-=1
							aiming = 0
							aim_pos = [0,0]
							aimed = 0
							shot_success = 1
						is_enemy_moving = 1
						ship_aim_pos,aim_message = aim.aim_message()
						fire_alert = 0
	
			if event.type == my_event_IDs["aim_response"]:
				pygame.time.set_timer(my_event_IDs["aim_response"],0)
				if aim_pos != ship_aim_pos or shot_success == 0:
					channel = pygame.mixer.find_channel()
					channel.play(missed_shot)
					while channel.get_busy():
						continue
					is_enemy_moving = 1
					ship_aim_pos,aim_message = aim.aim_message()
				shot_success = 0
				aiming = 0
	
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
	
	
	