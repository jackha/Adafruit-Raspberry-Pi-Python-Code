#!/usr/bin/python

from rpstomp import SevenSegmentPlus
from rpstomp import EightByEightPlus
import smiley
from time import sleep

grid = EightByEightPlus(address=0x70, brightness=0)
segment = SevenSegmentPlus(address=0x74, brightness=0)

segment.write('bye ')
grid.grid_array(smiley.smiley_cry)

cycle = [1,2,4,8,16,32]
cycle_counter = 0

# Display animation while shutting down.
while True:
    segment.writeDigitRaw(4, cycle[cycle_counter])
    cycle_counter = (cycle_counter + 1) % len(cycle)
    sleep(0.2)