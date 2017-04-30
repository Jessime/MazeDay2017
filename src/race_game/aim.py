import random

def aim_message():

	# Define vertical and horizontal directions
	# from the player's perspective
	h_dir = random.choice(("left","right"))
	v_dir = random.choice(("up","down"))

	# Define the offsets in the given directions
	h_offset = random.randint(1,3)
	v_offset = random.randint(1,3)

	aim_message = [h_dir,h_offset,v_dir,v_offset]

	# make offsets negative when appropriate
	if h_dir == "left":
		h_offset = -(h_offset)
	if v_dir == "down":
		v_offset = -(v_offset)
	ship_offset = [h_offset,v_offset]

	return (ship_offset,aim_message)

if __name__ == "__main__":
	aim_message()