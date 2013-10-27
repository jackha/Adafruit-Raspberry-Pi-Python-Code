# test rotary encoder and displays
import rotary_encoder
import threading
from Adafruit_LEDBackpack.Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack.Adafruit_8x8 import EightByEight

# react on ctrl-c
import signal 
import sys
def signal_handler(signal, frame):
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

A_PIN = 5  # use wiring pin numbers here
B_PIN = 4
#encoder = rotary_encoder.RotaryEncoder(A_PIN, B_PIN)
encoder_thread = rotary_encoder.RotaryEncoder.Worker(A_PIN, B_PIN)
encoder_thread.start()


class EightByEightPlus(EightByEight):
    """Better Eight By Eight by being smarter"""
    def __init__(self, *args, **kwargs):
        result = super(EightByEightPlus, self).__init__(*args, **kwargs)

        return result

    def set_values(self, values, selected=0):
        lookup_add = [2, 4, 8, 16, 32, 64, 128]
        print 'display values'
        for row in range(0, 8):
            row_value = 1 if row == selected else 0
            #for col in range(0, 7):
            #    if values[row] < col * 10:
            #        row_value += lookup_add[col]
            print 'row, rowvalue %d %d' % (row, row_value)
            grid.writeRowRaw(row, row_value, update=False)
        grid.disp.writeDisplay()


class SevenSegmentPlus(SevenSegment):
    pass

grid = EightByEightPlus(address=0x70)
segment = SevenSegmentPlus(address=0x74)

values = 8*[0]
selected = 0

print 'Test display and rotary encoder'

while(True):

    # read rotary encoder
    delta = encoder_thread.get_delta()

    if delta != 0:
        values[selected] += delta
        value = values[selected]
        print 'change value: %s delta %d' % (value, delta) 
    	
        # Set 7 segment
        # Set hours
        segment.writeDigit(0, int(value/1000)%10)
        segment.writeDigit(1, int(value/100)%10) 
        # Set minutes
        segment.writeDigit(3, int(value / 10) % 10)   # Tens
        segment.writeDigit(4, value % 10)        # Ones
        # Toggle color
        #segment.setColon(0)              # Toggle colon at 1Hz

        #for x in range(0, 8):
        #   for y in range(0, 8):
        #       color = 1 if (y*8+x) < value else 0
        #       grid.setPixel(x, y, color)
        grid.set_values(values)
    # sleep(0.001)
