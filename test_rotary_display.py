# test rotary encoder and displays
import rotary_encoder
from Adafruit_LEDBackpack.Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack.Adafruit_8x8 import EightByEight

A_PIN = 5  # use wiring pin numbers here
B_PIN = 4
encoder = rotary_encoder.RotaryEncoder(A_PIN, B_PIN)

grid = EightByEight(address=0x70)
segment = SevenSegment(address=0x74)

value = 0

while(True):

	# read rotary encoder
	value += encoder.get_delta()

	# Set 7 segment
	# Set hours
	segment.writeDigit(0, int(value/10000%10000)     # Tens
	segment.writeDigit(1, int(value/1000)%1000)          # Ones
	# Set minutes
	segment.writeDigit(3, int(value / 100) % 100)   # Tens
	segment.writeDigit(4, value % 10)        # Ones
	# Toggle color
	segment.setColon(0)              # Toggle colon at 1Hz

	for x in range(0, 8):
    	for y in range(0, 8):
    		color = 1 if (y*8+x) < value else 0
      		grid.setPixel(x, y, color)

	# sleep(0.001)