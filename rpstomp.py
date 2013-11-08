
# test rotary encoder and displays
import socket
import rotary_encoder
import threading
import datetime
import wiringpi2

from server import server
from time import sleep
from subprocess import Popen
import settings
import smiley
from mcp3008 import Mcp3008
from display import EightByEightPlus, SevenSegmentPlus, SPIRAL_DISPLAY
from effects import Effects

import os
from scroller import Scroller

# react on ctrl-c
import signal 
import sys
def signal_handler(signal, frame):
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


ENC1_PIN_A = 7  # use wiring pin numbers here
ENC1_PIN_B = 0
#ENC1_PIN_C = 6  # Push button

ENC2_PIN_A = 3  # use wiring pin numbers here
ENC2_PIN_B = 12
#ENC2_PIN_C = 3  # Push button

PUSH_BUTTON_PINS = [2, 13, 16, 1, 15, 4]

EIGHT_BY_EIGHT_ADDRESS = 0x70
EIGHT_BY_EIGHT_BRIGHTNESS = 0

SEVEN_SEGMENT_ADDRESS= 0x74
SEVEN_SEGMENT_BRIGHTNESS = 0

SLEEP_TIME = 0.02  # In seconds: give audio more time.
SLEEP_TIME_ROTARY = 0.005
SCROLLER_DELAY = 0.1  # Time before scrolling 1 pixel
SCROLLER_PRE_DELAY = 1  # Show before scrolling


# For the Mcp3008
SPICLK = 5
SPIMISO = 6
SPIMOSI = 10
SPICS = 11


# These should be files in pd directory (without .pd extension). Keys are displayed names
# The effects must all have 2 audio inlets and 8 normal inlets, 2 audio outlets and 1 normal outlet
OFF_EFFECT = {'display_name': '....', 'patch_name': '0', 'settings': []}

AVAILABLE_EFFECTS = [
#    {'display_name': 'test', 'full_name': 'test', 'patch_name': '14', 'settings': settings.diy2pitch},
    {'display_name': ' dly', 'full_name': 'delay', 'patch_name': '1', 'settings': settings.spectraldelay},
    {'display_name': 'vibr', 'full_name': 'step vibrato', 'patch_name': '2', 'settings': settings.stepvibrato},
#    {'display_name': 'syth', 'patch_name': '3', 'settings': settings.synth},
    {'display_name': 'pith', 'full_name': 'pitch', 'patch_name': '12', 'settings': settings.whammy},
    {'display_name': 'hexi', 'full_name': 'hexxiter', 'patch_name': '4', 'settings': settings.hexxiter},
    {'display_name': 'ring', 'full_name': 'ringmodulator', 'patch_name': '5', 'settings': settings.ringmodulator},
    {'display_name': 'revb', 'full_name': 'reverb', 'patch_name': '6', 'settings': settings.reverb},
    {'display_name': 'bold', 'full_name': 'bold as love', 'patch_name': '7', 'settings': settings.boldaslove},
#    {'display_name': 'psyn', 'patch_name': '8', 'settings': []},
    {'display_name': 'wird', 'full_name': 'weird', 'patch_name': '9', 'settings': settings.weird},
#    {'display_name': 'robo', 'patch_name': '10', 'settings': []},
    {'display_name': 'bsyn', 'full_name': 'binary synth', 'patch_name': '11', 'settings': []},
]


# Communication with Pd
class Communication():
    def __init__(self, *args, **kwargs):
        self.changes = False
        self.message = None

    def set(self, message):
        print 'echo %s from pd server' % message
        self.message = message
        self.changes = True
        #self.sock.sendall(message)  # echo all messages

    def get(self):
        message = self.message
        changes = self.changes
        self.changes = False
        self.message = None
        return changes, message


class ListenThread(threading.Thread):
    """Listen to incoming events from Pd patch"""
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


class Pd(object):
    """ Start a given patch.
    """
    def __init__(self):
        self.pd_proc = Popen("pd-extended -jack -nogui pd/loader.pd", 
            shell=True, preexec_fn=os.setsid)

    def shutdown(self):
        print 'stopping Pd %r...' % self.pd_proc.pid
        os.killpg(self.pd_proc.pid, signal.SIGTERM)


if __name__ == '__main__':
    print "Raspberry-Stomp"

    #pd = Pd()
    #sleep(2)  # TODO: improve
    #print "Starting Pd-extended..."
    #pd = Pd()
    #pd.start();
    #pd_proc = Popen("pd-extended -jack -nogui pd/server.pd", shell=True, preexec_fn=os.setsid)
    #sleep(2)

    grid = EightByEightPlus(
        address=EIGHT_BY_EIGHT_ADDRESS, 
        brightness=EIGHT_BY_EIGHT_BRIGHTNESS)
    segment = SevenSegmentPlus(
        address=SEVEN_SEGMENT_ADDRESS, 
        brightness=SEVEN_SEGMENT_BRIGHTNESS)

    values = 8*[0]
    selected = 0
    selected_idx = 0

    #encoder = rotary_encoder.RotaryEncoder(A_PIN, B_PIN)
    encoder1 = rotary_encoder.RotaryEncoder.Worker(
       ENC1_PIN_A, ENC1_PIN_B, sleep_time=SLEEP_TIME_ROTARY)
    encoder1.start()

    encoder2 = rotary_encoder.RotaryEncoder.Worker(
       ENC2_PIN_A, ENC2_PIN_B, sleep_time=SLEEP_TIME_ROTARY)
    encoder2.start()

    push_buttons = PushButtons(PUSH_BUTTON_PINS)

    # We use this socket to switch patches
    loader_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    loader_socket.connect(('localhost', 5000))
    effects = Effects(loader_socket, AVAILABLE_EFFECTS, OFF_EFFECT)
    
    #sleep(0.1)  # essential! Or Pd will sometimes stop with a segmentation fault.
    #send_sock = init_pd_socket()

    print "listen to Pd..."
    # Listen to Pd
    communication = Communication()
    server_thread = ListenThread(communication=communication)  # listen to messages from Pd
    server_thread.daemon = True
    server_thread.start()

    #initialized = False
    disp_needs_updating = True
    segment_needs_updating = True

    now = datetime.datetime.now()
    disp_timer_expiration = now
    segment_timer_expiration = now
    quit_timer_expiration = now
    push = {}
    pushed_in = {}  # You want to trigger a push only once.
    for i in range(len(PUSH_BUTTON_PINS)):
        pushed_in[i] = False

    running = True
    mcp = Mcp3008(SPICLK, SPIMISO, SPIMOSI, SPICS)
    mcp_values = 8*[0]
    scroller = None
    scroller_timer_expiration = now


    push3_timer_expiration = None
    hi_res_mode = False  # For ENC1, push to activate
    setting_switcher = True # For ENC2, push to switch to 'setting B' mode
    preset_forward = True  # For middle footswitch, which way to advance

    while(running):
        # read rotary encoder
        # delta1 = 0
        # delta2 = 0
        delta1 = encoder1.get_delta()
        delta2 = encoder2.get_delta()
        now = datetime.datetime.now()

        # Get 8 analog inputs, yeah!
        for i in range(8):
            mcp_values[i] = mcp.read(i)
        #segment.writeValue(mcp_values[7])
        # test
        #effects.setting(0, value=mcp_values[1]/1024.)

        #some_push = False
        for i in range(len(PUSH_BUTTON_PINS)):
            push[i] = push_buttons.get_button(i)
            #if push[i]:
            #    some_push = True

        comm_changes, comm_msg = communication.get()

        if comm_changes:
            print "TODO: Do something with %r" % comm_msg

        # Switch hi-res-mode
        if push[0] and not pushed_in[0]:
            hi_res_mode = not hi_res_mode
            scroller = Scroller('hi' if hi_res_mode else 'lo')
            scroller.reset()
            grid.bytes_array(scroller.up())
            disp_timer_expiration = now + datetime.timedelta(seconds=2)
            scroller_timer_expiration = now + datetime.timedelta(seconds=2)
            disp_needs_updating = True
            pushed_in[0] = True

        # Switch 'setting switcher' and 'setting b'
        if push[1] and not pushed_in[1]:
            setting_switcher = not setting_switcher
            scroller = Scroller('set' if setting_switcher else 'b')
            scroller.reset()
            grid.bytes_array(scroller.up())
            disp_timer_expiration = now + datetime.timedelta(seconds=2)
            scroller_timer_expiration = now + datetime.timedelta(seconds=SCROLLER_PRE_DELAY)
            disp_needs_updating = True
            pushed_in[1] = True

        # Effect on/off
        if push[2] and not pushed_in[2]:
            effects.effect_on_off()
            pushed_in[2] = True
            disp_needs_updating = True

        # up or down. Hold to switch direction
        if push[3] and not pushed_in[3]:
            push2_timer_expiration = now + datetime.timedelta(seconds=2)
            pushed_in[3] = True

        if pushed_in[3] and now > push2_timer_expiration:
            preset_forward = not preset_forward
            # Put the activation in the fast future 'easter egg'
            push2_timer_expiration += datetime.timedelta(days=1)
            scroller = Scroller('>>>' if preset_forward else '<<<')
            scroller.reset()
            grid.bytes_array(scroller.up())
            disp_timer_expiration = now + datetime.timedelta(seconds=2)
            scroller_timer_expiration = now + datetime.timedelta(seconds=2)
            disp_needs_updating = True

        # Button up triggers the preset switching
        if not push[3] and pushed_in[3]:
            if preset_forward:
                effects.up()
            else:
                effects.down()
            selected = 0
            selected_idx = 0
            segment_needs_updating = True
            disp_needs_updating = True

        # if push[4] and not pushed_in[4]:
        #     effects.up()
        #     selected = 0
        #     selected_idx = 0
        #     pushed_in[4] = True
        #     segment_needs_updating = True
        #     disp_needs_updating = True

        # Quit button
        if push[5] and not pushed_in[5]:
            #running = False;
            pushed_in[5] = True
            quit_timer_expiration = now + datetime.timedelta(seconds=2)
            grid.grid_array(smiley.smiley_uhoh)
            #send_sock.sendall('b_e bla;')

        if push[5] and pushed_in[5] and now <= quit_timer_expiration:
            seconds_left = (quit_timer_expiration - now).seconds + 1 # It's always < 60 sec
            segment.write('t % 2d' % (-seconds_left))

        if push[5] and pushed_in[5] and now > quit_timer_expiration:
            running = False

        if not push[5] and pushed_in[5]:
            # Just released button
            segment_needs_updating = True
            disp_needs_updating = True

        for i in range(len(PUSH_BUTTON_PINS)):
            if not push[i]:
                pushed_in[i] = False

        if delta1 != 0:
            scroller = None
            if len(effects.settings) == 0:
                continue
            if hi_res_mode:
                effects.setting(selected_idx, delta=delta1/4.)
            else:
                effects.setting(selected_idx, delta=delta1)

            # Set 7 segment
            value = 1000*effects.setting_norm(selected_idx)
            segment.writeValue(value)
            grid.special(
                64*effects.setting_norm(selected_idx), 
                matrix=effects.settings[selected_idx].get('display', SPIRAL_DISPLAY))

            disp_timer_expiration = datetime.datetime.now() + datetime.timedelta(seconds=2)
            segment_timer_expiration = disp_timer_expiration
            disp_needs_updating = True
            segment_needs_updating = True

        if delta2 != 0:
            scroller = None
            if len(effects.settings) == 0:
                continue
            selected = selected + delta2
            if selected > len(effects.settings)*8-1: # *8 make it slower
                selected = len(effects.settings)*8-1  
            if selected < 0:
                selected = 0
            selected_idx = selected/8

            grid.bytes_array(effects.settings_as_eight(selected=selected_idx))
            disp_timer_expiration = datetime.datetime.now() + datetime.timedelta(seconds=2)
            disp_needs_updating = True

            segment.write(effects.settings[selected_idx].get('name', 'set '))
            segment_timer_expiration = disp_timer_expiration
            segment_needs_updating = True

        # grid scroller
        if scroller is not None and now > scroller_timer_expiration:
            grid.bytes_array(scroller.up())
            scroller_timer_expiration = now + datetime.timedelta(seconds=SCROLLER_DELAY)

        # grid display: default view
        if now > segment_timer_expiration and segment_needs_updating:
            # default view for segment
            segment.write(effects.display_name)
            segment_needs_updating = False

        if now > disp_timer_expiration and disp_needs_updating:
            scroller = None
            #segment.write(effects.display_name)
            if effects.effect_on:
                grid.grid_array(smiley.smiley)
            else:
                grid.grid_array(smiley.smiley_sleep)
            disp_needs_updating = False
            push_timer_expiration = now

        sleep(SLEEP_TIME)

    #send_sock.sendall('volume 0;')
    effects.unload()
    grid.grid_array(smiley.smiley_cry)
    segment.write(' bye')

