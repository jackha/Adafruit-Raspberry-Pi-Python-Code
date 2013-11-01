# test rotary encoder and displays
import socket
import rotary_encoder
import threading
import datetime
import wiringpi2
from Adafruit_LEDBackpack.Adafruit_7Segment import SevenSegment
from Adafruit_LEDBackpack.Adafruit_8x8 import EightByEight

from server import server
from time import sleep

# react on ctrl-c
import signal 
import sys
def signal_handler(signal, frame):
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


ENC1_PIN_A = 5  # use wiring pin numbers here
ENC1_PIN_B = 4
#ENC1_PIN_C = 6  # Push button

ENC2_PIN_A = 0  # use wiring pin numbers here
ENC2_PIN_B = 2
#ENC2_PIN_C = 3  # Push button

PUSH_BUTTON_PINS = [6, 3, 12, 7, 14]

EIGHT_BY_EIGHT_ADDRESS = 0x70
EIGHT_BY_EIGHT_BRIGHTNESS = 0

SEVEN_SEGMENT_ADDRESS= 0x74
SEVEN_SEGMENT_BRIGHTNESS = 0

SLEEP_TIME = 0.02  # In seconds: give audio more time.
SLEEP_TIME_ROTARY = 0.005

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
            grid.writeRowRaw(row, row_value, update=False)
        grid.disp.writeDisplay()

    def grid_array(self, arr):
        """Grid array"""
        lookup_add = [128, 1, 2, 4, 8, 16, 32, 64]
        
        for y in range(8):
            byte_value = 0
            for x in range(8):
                byte_value += lookup_add[x] * arr[y][x]
                #grid.setPixel(x, y, arr[y][x])
            grid.writeRowRaw(y, byte_value, update=False)
        grid.disp.writeDisplay()


class SevenSegmentPlus(SevenSegment):
    def __init__(self, brightness=15, *args, **kwargs):
        result = super(SevenSegmentPlus, self).__init__(*args, **kwargs)
        self.disp.setBrightness(brightness)
        return result


"""For Janita: make smiley on display"""
smiley = [
    [0,0,1,1,1,1,0,0],
    [0,1,0,0,0,0,1,0],
    [1,0,1,0,0,1,0,1],
    [1,0,1,0,0,1,0,1],
    [1,1,0,0,0,0,1,1],
    [1,0,1,1,1,1,0,1],
    [0,1,0,0,0,0,1,0],
    [0,0,1,1,1,1,0,0]]

janita = [
    [1,0,1,0,1,0,0,0],
    [1,1,1,0,1,0,0,0],
    [1,0,1,0,1,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,1,0,0,1,0,0],
    [0,0,1,0,1,0,1,0],
    [1,0,1,0,1,1,1,0],
    [0,1,0,0,1,0,1,0]]

janita2 = [
    [1,0,0,1,0,1,0,0],
    [1,1,0,1,0,1,0,0],
    [1,0,1,1,0,1,0,0],
    [1,0,0,1,0,1,0,0],
    [0,0,0,0,0,0,1,0],
    [0,1,1,1,0,1,0,1],
    [0,0,1,0,0,1,1,1],
    [0,0,1,0,0,1,0,1]]

smiley_neutral = [
    [0,0,1,1,1,1,0,0],
    [0,1,0,0,0,0,1,0],
    [1,0,1,0,0,1,0,1],
    [1,0,1,0,0,1,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1],
    [0,1,0,0,0,0,1,0],
    [0,0,1,1,1,1,0,0]]


# Communication with Pd
class Communication():
    def __init__(self, sock, *args, **kwargs):
        self.sock = sock

    def set(self, message):
        print 'echo %s' % message
        #self.sock.sendall(message)  # echo all messages


class ListenThread(threading.Thread):
    """Listen to incoming events from Pd"""
    def __init__(self, communication, *args, **kwargs):
        self.communication = communication
        super(ListenThread, self).__init__(*args, **kwargs)

    def run(self):
        print "Start listening to Pd..."
        server('localhost', 3001, communication=self.communication)
        print "Stopped listening to Pd."


class PushButtons(object):
    def __init__(self, button_pins, sleep_time=0.05):
        self.gpio = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)
        self.button_pins = button_pins

        for button_pin in self.button_pins:
            self.gpio.pinMode(button_pin, self.gpio.INPUT)
            self.gpio.pullUpDnControl(button_pin, self.gpio.PUD_UP)

    def get_button(self, index):
        return self.gpio.digitalRead(self.button_pins[index]) == wiringpi2.GPIO.LOW


if __name__ == '__main__':
    print "Starting Raspberry-Stomp..."

    grid = EightByEightPlus(
        address=EIGHT_BY_EIGHT_ADDRESS, 
        brightness=EIGHT_BY_EIGHT_BRIGHTNESS)
    segment = SevenSegmentPlus(
        address=SEVEN_SEGMENT_ADDRESS, 
        brightness=SEVEN_SEGMENT_BRIGHTNESS)

    values = 8*[0]
    selected = 0
    startup = True

    #encoder = rotary_encoder.RotaryEncoder(A_PIN, B_PIN)
    encoder1 = rotary_encoder.RotaryEncoder.Worker(
        ENC1_PIN_A, ENC1_PIN_B, sleep_time=SLEEP_TIME_ROTARY)
    encoder1.start()

    encoder2 = rotary_encoder.RotaryEncoder.Worker(
        ENC2_PIN_A, ENC2_PIN_B, sleep_time=SLEEP_TIME_ROTARY)
    encoder2.start()

    push_buttons = PushButtons(PUSH_BUTTON_PINS)

    # Create a socket (SOCK_STREAM means a TCP socket)
    # client of puredata: use 'netreceive 3000' in pd
    print "init send socket to Pd..."
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_sock.connect(('localhost', 3000))

    print "listen to Pd..."
    # Listen to Pd
    communication = Communication(sock=send_sock)
    #server_thread = ListenThread(communication=communication)  # listen to messages from Pd
    #server_thread.daemon = True
    #server_thread.start()

    sleep(1)
    print "init to Pd..."
    send_sock.sendall('init;')  # makes Pd connect back on port 3001

    push_timer_expiration = datetime.datetime.now()

    # Option names in Pd.
    option_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    #initialized = False
    grid_needs_updating = False
    push = {}

    while(True):
        # read rotary encoder
        delta1 = encoder1.get_delta()
        delta2 = encoder2.get_delta()

        #some_push = False
        for i in range(len(PUSH_BUTTON_PINS)):
            push[i] = push_buttons.get_button(i)
            #if push[i]:
            #    some_push = True

        if push[0]:
            push_timer_expiration = datetime.datetime.now() + datetime.timedelta(seconds=2)
            grid.grid_array(janita)
	    grid_needs_updating = True

        if push[1]:
            push_timer_expiration = datetime.datetime.now() + datetime.timedelta(seconds=2)
            grid.grid_array(janita2)
	    grid_needs_updating = True

        if push[2] or push[3] or push[4]:
            push_timer_expiration = datetime.datetime.now() + datetime.timedelta(seconds=2)
            grid.grid_array(smiley)
	    grid_needs_updating = True
	    print push

	    if push[2]:
            send_sock.sendall('test algorithm;')
            # testing shutdown
            #import os
            #os.system("shutdown now -h -k")

        if delta1 != 0 or delta2 != 0 or startup:
            selected = (selected + delta2) % (8*8)  # make it slower
            selected_idx = selected/8
            values[selected_idx] += delta1
            value = values[selected_idx]
            print 'change value: selected %s(%s) value %s delta1 %d delta2 %d' % (
                selected_idx, selected, value, delta1, delta2) 
            
            #if push1 or push2:
            #    push_timer_expiration = datetime.datetime.now() + datetime.timedelta(seconds=4)

            #if push1 and not initialized:
            #    print "init to Pd..."
            #    send_sock.sendall('init;')  # makes Pd connect back on port 3001
            #    initialized = True

            #if push2:
            #    print 'sending la la...'
            #    send_sock.sendall('la la;')

            # Set 7 segment
            # Set hours
            segment.writeDigit(0, int(value/1000)%10)
            segment.writeDigit(1, int(value/100)%10) 
            # Set minutes
            segment.writeDigit(3, int(value / 10) % 10)   # Tens
            segment.writeDigit(4, value % 10)        # Ones
            # Toggle color
            #segment.setColon(0)              # Toggle colon at 1Hz

            # send test message to Pd server
            #print "Volume to Pd..."
            #send_sock.sendall('volume %f;' % (value*0.001))

            print "Option %d %s: %s" % (selected_idx, option_names[selected_idx], str(value))
            send_sock.sendall('%s %d;' % (option_names[selected_idx], values[selected_idx]))

            startup = False
            grid_needs_updating = True

        # grid display: default view
        if datetime.datetime.now() > push_timer_expiration and grid_needs_updating:
            grid.set_values(values, selected=selected_idx)
            grid_needs_updating = False
            push_timer_expiration = datetime.datetime.now()

        sleep(SLEEP_TIME)
