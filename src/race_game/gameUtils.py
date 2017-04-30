def play_directional_sound(sound_name,channel_name,left,right):
	"""This function allows sound to be played at a specified position between the two speakers.
	The function parameters are:
	sound_name: the name of the sound object to be played (string).
	channel: the name of the channel through which the sound will be played (string).
	left: the volume of the sound in the left speaker float from 0-1).
	right: the volume of the sound in the right speaker (float from 0-1).

	For example, sound can be played completely through the left speaker
	by setting left to a positive number and right to 0.
	The function will only attempt to play sound through 
	the specified channel if no other sounds are already playing.
	This is because only one sound can be played through
	a channel at once.
	Attempting to play a sound on the channel before the a prior sound has finished
	will force the new sound to a different channel
	that will likely not have the same sound position as the target channel."""

	if not channel_name.get_busy():
		channel_name.set_volume(left,right)
		channel_name.play(sound_name)
	return

def play_single_sound(channel,sound):
	channel.play(sound)
	while channel.get_busy():
		continue
	return
