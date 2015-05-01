#!/usr/bin/python
# Copyright (c) 2015 Massimo Gaggero
# Author: Massimo Gaggero
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Uncomment to enable debug output:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import Adafruit_HTU21D.HTU21D as HTU21D

# Default constructor will pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.
sensor = HTU21D.HTU21D()

# Optionally you can override the bus number:
#sensor = HTU21D.HTU21D(busnum=2)

# You can also optionally change the HTU21D mode to one of HTU21D_HOLDMASTER, HTU21D_NOHOLDMASTER.
# See the HTU21D datasheet for more details on the meanings of each mode (accuracy and power consumption
# are primarily the differences).  The default mode is HTU21D_HOLDMASTER.
#sensor = HTU21D.HTU21D(mode=HTU21D.HTU21D_HOLDMASTER)

print 'Temp = {0:0.2f} *C'.format(sensor.read_temperature())
print 'Humidity  = {0:0.2f} %'.format(sensor.read_humidity())
print 'Dew Point = {0:0.2f} *C'.format(sensor.read_dewpoint())
