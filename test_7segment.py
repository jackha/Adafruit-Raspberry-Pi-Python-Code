#!/usr/bin/python

import time
import datetime
from Adafruit_LEDBackpack.Adafruit_7Segment import SevenSegment

# ===========================================================================
# Clock Example
# ===========================================================================
segment = SevenSegment(address=0x74)

print "Press CTRL+Z to exit"

c = 0
# Continually update the time on a 4 char, 7-segment display
# Continually update the 8x8 display one pixel at a time


# Set hours
segment.writeDigitRaw(0, 0x00)   
segment.writeDigitRaw(1, 0x01)          # Ones
# Set minutes
segment.writeDigitRaw(3, 0x02)   # Tens
segment.writeDigitRaw(4, 0x03)        # Ones
# Toggle color
segment.setColon(1)              # Toggle colon at 1Hz

