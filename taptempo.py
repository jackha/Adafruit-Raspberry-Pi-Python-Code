#taptempo
import datetime

class TapTempo(object):
	def __init__(self):
		self.timer = 0
		past = datetime.datetime.now() - datetime.timedelta(seconds=10)
		self.last_tap = past
		self.timer_start = past
		self.tap_counter = 0

	def tap(self):
		now = datetime.datetime.now()
		if self.last_tap < now - datetime.timedelta(seconds=3):
			# reset
			self.timer_start = now
			self.last_tap = now
			self.tap_counter = 0
		else:
			self.last_tap = now
			self.tap_counter += 1

	def seconds(self):
		if self.tap_counter == 0:
			return 1.
		now = datetime.datetime.now()
		delta_time = (now - self.timer_start)
		delta_time_seconds = delta_time.seconds + delta_time.microseconds/1000000.
		seconds = float(delta_time_seconds) / self.tap_counter
		return seconds

	def bpm(self):
		return 60 / self.seconds()


if __name__ == '__main__':
	from time import sleep
	tt = TapTempo()
	tt.tap()
	sleep(.5)
	tt.tap()
	print tt.bpm()
	sleep(.6)
	tt.tap()
	print tt.bpm()
	sleep(.4)
	tt.tap()
	print tt.bpm()

