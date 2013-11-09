#!/usr/bin/python

from rpstomp import SevenSegmentPlus
from rpstomp import EightByEightPlus
import smiley

grid = EightByEightPlus(address=0x70)
segment = SevenSegmentPlus(address=0x74)

segment.write(' bye')
segment.setColon(1)              # Toggle colon at 1Hz

grid.grid_array(smiley.smiley_cry)