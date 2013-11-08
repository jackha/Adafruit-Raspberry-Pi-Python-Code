#!/usr/bin/python
import datetime
from font import font

class Scroller(object):

    def __init__(self, text):
        self.text = text
        self.scroll_array = [[],[],[],[],[]]
        self.char_height = len(self.scroll_array)
        # build scroll array using font
        for character in text:
            for idx, row in enumerate(font[character.lower()]):
                self.scroll_array[idx].extend(row + [0])

        self.max_pos = len(self.scroll_array[0])
        self.pos = 0
        self.byte_array = self.char_height * [0]  # for sending to display

    def up(self, autorestart=False):
        """move 1 pixel"""
        byte_array_for_display = []
        for idx in range(self.char_height):
            self.byte_array[idx] >>= 1  # shift 1 pixel
            if self.pos < self.max_pos:
                self.byte_array[idx] += 128*self.scroll_array[idx][self.pos]
            # Byte array for display has weird bit ordering: [128, 1, 2, 4, 8, 16, 32, 64]
            byte_array_for_display.append((self.byte_array[idx] >> 1) + (128*(self.byte_array[idx] & 1)))
            #byte_array_for_display.append(self.byte_array[idx])

        self.pos += 1
        if autorestart:
            self.pos %= self.max_pos
        return byte_array_for_display + [0,0,0]

    def reset(self):
        self.pos = 0
        self.byte_array = self.char_height * [0]  # for sending to display
        for i in range(7):
            self.up()

    def timedelta(self, delta):
        """time that it takes for the whole text. delta in seconds, it's just a guess """
        return (8+len(self.scroll_array[0])) * (delta + 0.03)

    # def arr(self, pos):
    #     result = []
    #     pos = pos % (self.max_pos)
    #     for row in self.scroll_test:
    #         result.append(row[pos:pos+8])
    #     return result


if __name__=='__main__':
    import time
    from rpstomp import EightByEightPlus
    pos = 0
    grid = EightByEightPlus(address=0x70, brightness=0)

    scroller = Scroller(':-)   ;-)   (*^.^*)    ^.^    ')

    while(True):
        pos += 1

        grid.bytes_array(scroller.up())

        time.sleep(0.02)
