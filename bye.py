#!/usr/bin/python

from rpstomp import SevenSegmentPlus
from rpstomp import EightByEightPlus
import smiley

grid = EightByEightPlus(address=0x70, brightness=0)
segment = SevenSegmentPlus(address=0x74, brightness=0)

segment.write('byee')
grid.grid_array(smiley.smiley_cry)