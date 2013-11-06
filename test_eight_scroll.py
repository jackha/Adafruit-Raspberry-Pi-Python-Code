#!/usr/bin/python

import time
import datetime
from rpstomp import EightByEightPlus
from scroller import Scroller
        

pos = 0
grid = EightByEightPlus(address=0x70, brightness=0)

scroller = Scroller()

while(True):
    pos += 1

    grid.bytes_array(scroller.up())

    time.sleep(0.1)
