Raspberry Pi Stompbox
---------------------

features (a lot of TODO's)::

- 7 segment display to show current "program"
- 8x8 LED matrix to show settings and animations
- 2 rotary encoders to change settings
- 3 footswitches: turn effect on/off, change program up/down
- use of an external audio interface (I use a Focusrite 2i2)
- expression pedal


Hardware used
-------------

- raspberry pi rev b
- Adafruit blue 7 segment display (address set to 0x74 by shorting A2)
- Adafruit 8x8 LED display (address 0x70)
- mcp3008 chip for the expression pedal

Pins
----

WiringPi has its own numbering scheme. Let's see what's what.


| WiringPi | Header | | WiringPi | 
| | 1 | 2 | |
   8        3      4    
   9        5      6
   7        7      8       15
            9      10      16
   0        11     12       1
   2        13     14
   3        15     16       4
            17     18       5
   12       19     20
   13       21     22       6
   14       23     24      10
            25     26      11


ENC1_PIN_A = 0  # use wiring pin numbers here
ENC1_PIN_B = 7
#ENC1_PIN_C = 6  # Push button

ENC2_PIN_A = 12  # use wiring pin numbers here
ENC2_PIN_B = 3
#ENC2_PIN_C = 3  # Push button

PUSH_BUTTON_PINS = [2, 13, 15, 16, 1, 4]

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


Hook up the displays
====================

See::

http://learn.adafruit.com/matrix-7-segment-led-backpack-with-the-raspberry-pi/hooking-everything-up

d and c are in parallel for the 2 displays.


Setting up your software
------------------------

OS
==

- install raspbian wheezy on an SD card (I used 2013-09-25-wheezy-raspbian)

http://www.raspberrypi.org/downloads

- git clone https://github.com/jackha/raspberry-stomp

- overclock /boot/config.txt

http://wiki.linuxaudio.org/wiki/raspberrypi

arm_freq=800
core_freq=350
sdram_freq=500
gpu_mem=16


JACK
====

Add audio repository::

wget -O - http://rpi.autostatic.com/autostatic.gpg.key| sudo apt-key add -
sudo wget -O /etc/apt/sources.list.d/autostatic-audio-raspbian.list http://rpi.autostatic.com/autostatic-audio-raspbian.list
sudo apt-get update

Install JACK (there is also a JACK2, for us it's no difference)

   $ sudo apt-get --no-install-recommends install jackd1


Displays
========

- enable i2c communication

    $ sudo nano /etc/modules

add 2 lines::

- i2c-bcm2708 
- i2c-dev

    $ sudo apt-get install python-smbus

Remove i2c devices from the blacklist::

    $ sudo nano /etc/modprobe.d/raspi-blacklist.conf

Comment out lines by placing a '#' before it::

# blacklist spi-bcm2708
# blacklist i2c-bcm2708


check if displays are OK::

    $ sudo i2cdetect -y 1

    Should display 70 and 74 somewhere

Setting permissions for the i2c devices::

    $ sudo nano /lib/udev/rules.d/60-i2c-tools.rules 

    change 0x660 to 0x666

After reboot it should display::

    $ ls -al /dev/i2c-*

crw-rw-rwT 1 root i2c 89, 0 Oct 27 13:08 /dev/i2c-0
crw-rw-rwT 1 root i2c 89, 1 Oct 27 13:08 /dev/i2c-1

Now you can interact with the displays without being superuser.


Rotary encoders
===============

We use the rotary encoder library from gaugette, which in turn uses wiringPi and WiringPi2::

    $ sudo apt-get install python-dev python-setuptools

### WiringPi and WiringPi2-Python

Modules that use GPIO require [wiringpi](https://projects.drogon.net/raspberry-pi/wiringpi/) and [WiringPi2-Python](https://github.com/WiringPi/WiringPi2-Python).

To install wiringpi:
```
git clone git://git.drogon.net/wiringPi
cd wiringPi
sudo ./build
```

To install wiringpi2-python:
```
git clone https://github.com/Gadgetoid/WiringPi2-Python.git
cd WiringPi2-Python/
sudo python setup.py install
cd ..
```


trying this::

    $ sudo apt-get install python-rpi.gpio 

https://code.google.com/p/raspberry-gpio-python/wiki/Examples

Audio interface
===============

See if it is listed::

$ cat /proc/asound/cards
 0 [ALSA           ]: BRCM bcm2835 ALSbcm2835 ALSA - bcm2835 ALSA
                      bcm2835 ALSA
 1 [USB            ]: USB-Audio - Scarlett 2i2 USB
                      Focusrite Scarlett 2i2 USB at usb-bcm2708_usb-1.3, high speed


Set the Alsa USB audio device to have priority 0::

    # sudo nano /etc/modprobe.d/alsa-base.conf

Change the line with snd-usb-audio to::

options snd-usb-audio index=0


$ speaker-test -c2 -D hw:0,0 -F S32_LE

(somehow only the sample format S32_LE works...)



Expression pedal
================

Mcp3008

    $ sudo easy_install rpi.gpio


Finishing up the software
=========================

Automatically startup and shut down::

$ sudo chmod 755 jackstart.sh

Add /home/pi/raspberry-stomp/jackstart.sh to /etc/rc.local

at the end, add 

$ halt


Background info
---------------

Started as a fork of::

Adafruit's Raspberry-Pi Python Code Library
  https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

Rotary encoder code from gaugette::

https://github.com/guyc/py-gaugette/blob/master/gaugette/rotary_encoder.py
