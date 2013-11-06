from time import sleep
from Adafruit_LEDBackpack.Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack.Adafruit_8x8 import EightByEight



class EightByEightPlus(EightByEight):
    """Better Eight By Eight by being smarter"""
    def __init__(self, brightness=15, *args, **kwargs):
        result = super(EightByEightPlus, self).__init__(*args, **kwargs)
        self.disp.setBrightness(brightness)
        return result

    def set_values(self, values, selected=0):
        lookup_add = [1, 2, 4, 8, 16, 32, 64]
        #print 'display values'
        for row in range(0, 8):
            # strangely 128 is the first pixel, not 1
            row_value = 128 if row == selected else 0
            for col in range(0, 7):
                if values[row] > col * 10:
                    row_value += lookup_add[col]
            #print 'row, rowvalue %d %d' % (row, row_value)
            self.writeRowRaw(row, row_value, update=False)
        self.disp.writeDisplay()

    def grid_array(self, arr):
        """Grid array"""
        lookup_add = [128, 1, 2, 4, 8, 16, 32, 64]
        
        for y in range(8):
            byte_value = 0
            for x in range(8):
                byte_value += lookup_add[x] * arr[y][x]
                #grid.setPixel(x, y, arr[y][x])
            self.writeRowRaw(y, byte_value, update=False)
        self.disp.writeDisplay()

    def bytes_array(self, arr):
        """Grid array, you may provide less than 8 rows"""
        for y in range(len(arr)):
            self.writeRowRaw(y, arr[y], update=False)
        self.disp.writeDisplay()


class SevenSegmentPlus(SevenSegment):
    letters = {
        ' ': 0,
        'a': 1 + 2 + 4 + 16 + 32 + 64,
        'b': 4 + 8 + 16 + 32 + 64,
        'c': 8 + 16 + 64,
        'd': 2 + 4 + 8 + 16 + 64,
        'e': 1 + 2 + 8 + 16 + 32 + 64,
        'f': 1 + 16 + 32 + 64,
        'g': 1 + 2 + 4 + 8 + 32 + 64,
        'h': 4 + 16 + 32 + 64,
        'i': 4,
        'j': 2 + 4 + 8 + 16,
        'k': 2 + 4 + 16 + 32 + 64,
        'l': 2 + 4,
        'm': 1 + 2 + 4 + 16 + 32,
        'n': 4 + 16 + 64,
        'o': 4 + 8 + 16 + 64,
        'p': 1 + 2 + 16 + 32 + 64,
        'q': 1 + 2 + 4 + 32 + 64,
        'r': 16 + 64,
        's': 1 + 4 + 8 + 32 + 64,
        't': 8 + 16 + 32 + 64,
        'u': 4 + 8 + 16,
        'v': 2 + 4 + 8 + 16 + 32,
        'w': 2 + 4 + 8 + 16 + 32,
        'x': 2 + 4 + 16 + 32 + 64,
        'y': 2 + 4 + 8 + 32 + 64,
        'z': 1 + 2 + 8 + 16 + 64,
        '0': 1 + 2 + 4 + 8 + 16 + 32,
        '1': 2 + 4,
        '2': 1 + 2 + 8 + 16 + 64,
        '3': 1 + 2 +4 + 8 + 64,
        '4': 2 + 4 + 32 + 64,
        '5': 1 + 4 + 8 + 32 + 64,
        '6': 4 + 8 + 16 + 32 + 64,
        '7': 1 + 2 + 4,
        '8': 1 + 2 + 4 + 8 + 16 + 32 + 64,
        '9': 1 + 2 + 4 + 8 + 32 + 64,
        '-': 64,
        '.': 128,
    }

    def __init__(self, brightness=15, *args, **kwargs):
        result = super(SevenSegmentPlus, self).__init__(*args, **kwargs)
        self.disp.setBrightness(brightness)
        return result

    def write(self, text):
        """Write text on display, must have 4 characters!"""
        text = text.lower()
        self.writeDigitRaw(0, self.letters[text[0]])
        self.writeDigitRaw(1, self.letters[text[1]])
        self.writeDigitRaw(3, self.letters[text[2]])
        self.writeDigitRaw(4, self.letters[text[3]])

    def writeValue(self, value):
        """Write integer to display"""

        self.writeDigit(0, int(value/1000)%10)
        self.writeDigit(1, int(value/100)%10) 
        # Set minutes
        self.writeDigit(3, int(value / 10) % 10)   # Tens
        self.writeDigit(4, int(value) % 10)        # Ones
        # Toggle color
        #segment.setColon(0)              # Toggle colon at 1Hz
