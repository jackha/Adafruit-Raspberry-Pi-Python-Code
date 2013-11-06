#!/usr/bin/python

import time
import datetime
from rpstomp import EightByEightPlus

grid = EightByEightPlus(address=0x70)


class Scroller(object):
    scroll_test = [
    [1,0,0,0,0,0,1,0,0,1,1,0,0,0,1,0],
    [0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,1],
    [0,0,1,0,0,1,1,1,0,1,1,0,0,1,0,0],
    [0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,1],
    [0,0,0,0,1,0,0,0,0,1,1,0,0,0,1,0],
    [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
    ]

    def __init__(self):
        self.max_pos = len(self.scroll_test) - 8

    def arr(self, pos):
        result = []
        pos = pos % (self.max_pos)
        for row in range(self.scroll_test):
            result.append(row[pos:pos+8])
        return result

pos = 0
# Continually update the time on a 4 char, 7-segment display
# Continually update the 8x8 display one pixel at a time
while(True):
    pos += 1

    grid_arr = scroller.arr(pos)
    grid.grid_array(grid_arr)

    time.sleep(0.1)