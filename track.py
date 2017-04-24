import random

def make_track(num_obst):
	"""This function constructs a race track of given number of obsticles.
	The track will be a dictionary with obsticle positions as keys and
	obsticle names as values."""

	track = {}

	# Make a tuple of the possible obsticles
	obst_types = ("left_turn","right_turn","left_turn","right_turn","laser")

	# Define the positions of the obsticles
	start_pos = random.randint(3,6)
	track_poses = []
	track_poses.append(start_pos)

	for i in range(1,num_obst):
		prev_pos = track_poses[i-1]
		cur_pos = prev_pos+random.randint(2,5)
		track_poses.append(cur_pos)

	# Randomly assign an obsticle to each position
	for i in track_poses:
		track[i] = random.choice(obst_types)

	return track

	