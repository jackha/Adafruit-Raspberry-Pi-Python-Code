#!/usr/bin/env python
import time
import os
import wiringpi2

class Mcp3008(object):
    def __init__(self, clockpin, misopin, mosipin, cspin):
        self.gpio = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)
        self.gpio.pinMode(clockpin, self.gpio.OUTPUT)
        self.gpio.pinMode(misopin, self.gpio.INPUT)
        self.gpio.pinMode(mosipin, self.gpio.OUTPUT)
        self.gpio.pinMode(cspin, self.gpio.OUTPUT)
        self.clockpin = clockpin
        self.misopin = misopin
        self.mosipin = mosipin
        self.cspin = cspin

    def read(self, adcnum):
        # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        self.gpio.digitalWrite(self.cspin, True)
        self.gpio.digitalWrite(self.clockpin, False)
        self.gpio.digitalWrite(self.cspin, False)

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here

        for i in range(5):
            if (commandout & 0x80):
                self.gpio.digitalWrite(self.mosipin, True)
            else:
                self.gpio.digitalWrite(self.mosipin, False)
            commandout <<= 1
            self.gpio.digitalWrite(self.clockpin, True)
            self.gpio.digitalWrite(self.clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
            self.gpio.digitalWrite(self.clockpin, True)
            self.gpio.digitalWrite(self.clockpin, False)
            adcout <<= 1
            if (self.gpio.digitalRead(self.misopin)):
                adcout |= 0x1

        self.gpio.digitalWrite(self.cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

if __name__ == '__main__':
    # change these as desired - they're the pins connected from the
    # SPI port on the ADC to the Cobbler
    # SPICLK = 24
    # SPIMISO = 25
    # SPIMOSI = 8
    # SPICS = 7

    SPICLK = 5
    SPIMISO = 6
    SPIMOSI = 10
    SPICS = 11

    mcp = Mcp3008(SPICLK, SPIMISO, SPIMOSI, SPICS)

    while True:
        print mcp.read(0)

        time.sleep(0.01)