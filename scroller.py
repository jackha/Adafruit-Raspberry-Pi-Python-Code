#!/usr/bin/python

import time
import datetime
from rpstomp import EightByEightPlus


class Scroller(object):
    font = {
        'a': [
            [1,1,0],
            [0,0,1],
            [0,1,1],
            [1,0,1],
            [0,1,1],
        ],
        'b': [
            [1,0,0],
            [1,0,0],
            [1,1,0],
            [1,0,1],
            [1,1,0],
        ],
        'c': [
            [0,1,0],
            [1,0,1],
            [1,0,0],
            [1,0,1],
            [0,1,0],
        ],
        'd': [
            [0,0,1],
            [0,0,1],
            [0,1,1],
            [1,0,1],
            [0,1,1],
        ],
        'e': [
            [0,1,0],
            [1,0,1],
            [1,1,0],
            [1,0,0],
            [0,1,1],
        ],
    }

    def __init__(self, text):
        self.text = text
        self.char_height = 5
        self.scroll_array = [[0],[0],[0],[0],[0]]
        # build scroll array using font
        for character in text:
            for idx, row in enumerate(self.font[character.lower()]):
                print idx, row
                self.scroll_array[idx].extend(row + [0])

        self.max_pos = len(self.scroll_array[0])
        self.pos = 0
        self.byte_array = self.char_height * [0]  # for sending to display
        print self.scroll_array

    def up(self):
        """move 1 pixel"""
        byte_array_for_display = []
        for idx in range(self.char_height):
            self.byte_array[idx] >>= 1  # shift 1 pixel
            self.byte_array[idx] += 128*self.scroll_array[idx][self.pos]
            # Byte array for display has weird bit ordering: [128, 1, 2, 4, 8, 16, 32, 64]
            #byte_array_for_display.append(self.byte_array[idx] << 1 + 128*self.byte_array[idx] & 1)
            byte_array_for_display.append(self.byte_array[idx])
        self.pos = (self.pos + 1) % self.max_pos
        print byte_array_for_display
        return byte_array_for_display


    # def arr(self, pos):
    #     result = []
    #     pos = pos % (self.max_pos)
    #     for row in self.scroll_test:
    #         result.append(row[pos:pos+8])
    #     return result


if __name__=='__main__':
    pos = 0
    grid = EightByEightPlus(address=0x70, brightness=0)

    scroller = Scroller('a')

    while(True):
        pos += 1

        grid.bytes_array(scroller.up())

        time.sleep(0.1)
