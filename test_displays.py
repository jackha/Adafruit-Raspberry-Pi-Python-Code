#!/usr/bin/python

import time
import datetime
from Adafruit_LEDBackpack.Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack.Adafruit_8x8 import EightByEight

# ===========================================================================
# 8x8 Pixel Example
# ===========================================================================
grid = EightByEight(address=0x70)

# ===========================================================================
# Clock Example
# ===========================================================================
segment = SevenSegment(address=0x74)

print "Press CTRL+Z to exit"

c = 0
# Continually update the time on a 4 char, 7-segment display
# Continually update the 8x8 display one pixel at a time
while(True):
  now = datetime.datetime.now()
  hour = now.hour
  minute = now.minute
  second = now.second
  # Set hours
  segment.writeDigit(0, int(hour / 10))     # Tens
  segment.writeDigit(1, hour % 10)          # Ones
  # Set minutes
  segment.writeDigit(3, int(minute / 10))   # Tens
  segment.writeDigit(4, minute % 10)        # Ones
  # Toggle color
  segment.setColon(second % 2)              # Toggle colon at 1Hz

  grid.setPixel(c % 8, c / 8)

  c = c + 1
  if c == 64:
    c = 0
    grid.clear()

  # Wait one second
  time.sleep(1)
