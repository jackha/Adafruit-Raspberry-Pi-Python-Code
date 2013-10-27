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


Hook up the displays
====================

See::

http://learn.adafruit.com/matrix-7-segment-led-backpack-with-the-raspberry-pi/hooking-everything-up

d and c are in parallel for the 2 displays.


Setting up your raspberry pi
----------------------------

OS
==

- install raspbian wheezy on an SD card (I used 2013-09-25-wheezy-raspbian)

http://www.raspberrypi.org/downloads


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


Background info
---------------

Started as a fork of::

Adafruit's Raspberry-Pi Python Code Library
  https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

Rotary encoder code from gaugette::

https://github.com/guyc/py-gaugette/blob/master/gaugette/rotary_encoder.py
