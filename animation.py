class Animation(object):
	"""Feed this object with 'frames' as pacman and ghost in smiley.py"""
	def __init__(self, frames):
		self.frames = frames
		self.frame_counter = 0

	def up(self):
		self.frame_counter = (self.frame_counter + 1) % len(self.frames)
		return self.frames[self.frame_counter]


if __name__ == '__main__':
	import smiley
	from time import sleep

	from rpstomp import EightByEightPlus
    grid = EightByEightPlus(address=0x70, brightness=0)

	animation1 = Animation(smiley.pacman)
	animation2 = Animation(smiley.ghost)
	for i in range(10):
		frame = animation1.up()
		grid.grid_array(frame)		
		sleep(0.1)
	for i in range(10):
		frame = animation2.up()
		grid.grid_array(frame)		
		sleep(0.1)
