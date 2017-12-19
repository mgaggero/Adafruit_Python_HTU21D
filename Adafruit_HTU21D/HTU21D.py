#!/usr/bin/env python

# The MIT License (MIT)
#
# Copyright (c) 2015-2017 Massimo Gaggero
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
HTU21D is a python library for the Adafruit HTU21D-F Humidity/Temperature
sensor breakout board.
"""

import io
import math
import time
import fcntl
import logging


# RPI-2/3 I2C DEFAULT BUS
I2C_BUS                   = 1

# RPI I2C SLAVE ADDRESS
I2C_SLAVE                 = 0x0703

# HTU21D default address
HTU21D_I2CADDR            = 0x40

# Operating Modes
HTU21D_HOLDMASTER         = 0x00
HTU21D_NOHOLDMASTER       = 0x10

# HTU21D Commands
HTU21D_TRIGGERTEMPCMD     = 0xE3  # Trigger Temperature Measurement
HTU21D_TRIGGERHUMIDITYCMD = 0xE5  # Trigger Humidity Measurement
HTU21D_WRITEUSERCMD       = 0xE6  # Write user register
HTU21D_READUSERCMD        = 0xE7  # Read user register
HTU21D_SOFTRESETCMD       = 0xFE  # Soft reset

HTU21D_MAX_MEASURING_TIME = 100   # mSec

# HTU21D Constants for Dew Point calculation
HTU21D_A = 8.1332
HTU21D_B = 1762.39
HTU21D_C = 235.66


class HTU21DException(Exception):
    pass


class HTU21DBusProtocol(object):
    def __init__(self, busnum = I2C_BUS, address = HTU21D_I2CADDR):
        self._busnum  = busnum
        self._address = address

        self._device_name = '/dev/i2c-{}'.format(self._busnum)

        self._read_handler  = None
        self._write_handler = None

    def open(self):
        self._read_handler  = io.open(self._device_name, 'rb', buffering=0)
        self._write_handler = io.open(self._device_name, 'wb', buffering=0)

        fcntl.ioctl(self._read_handler,  I2C_SLAVE, self._address)
        fcntl.ioctl(self._write_handler, I2C_SLAVE, self._address)

        time.sleep(HTU21D_MAX_MEASURING_TIME/1000)

    def send_command(self, command):
        self._write_handler.write(command.to_bytes(1, 'big'))

    def read_bytes(self, len):
        return self._read_handler.read(len)

    def close(self):
        self._read_handler.close()
        self._write_handler.close()


class HTU21D(object):
    def __init__(self, busnum=I2C_BUS, address=HTU21D_I2CADDR, mode=HTU21D_NOHOLDMASTER):
        self._logger = logging.getLogger('Adafruit_HTU21D.HTU21D')

        # Check that mode is valid.
        if mode not in [HTU21D_HOLDMASTER, HTU21D_NOHOLDMASTER]:
            raise ValueError('Unexpected mode value {0}.  Set mode to one of HTU21D_HOLDMASTER, HTU21D_NOHOLDMASTER'.format(mode))

        self._busnum  = busnum
        self._address = address
        self._mode    = mode

        # Create I2C device.
        self._htu_handler = HTU21DBusProtocol(self._busnum, self._address)

    def crc_check(self, msb, lsb, crc):
        remainder = ((msb << 8) | lsb) << 8
        remainder |= crc
        divsor = 0x988000

        for i in range(0, 16):
            if remainder & 1 << (23 - i):
                remainder ^= divsor
            divsor >>= 1

        if remainder == 0:
            return True
        else:
            return False

    def reset(self):
        """Reboots the sensor switching the power off and on again."""
        self._htu_handler.open()

        self._htu_handler.send_command(HTU21D_SOFTRESETCMD & 0xFF)
        time.sleep(HTU21D_MAX_MEASURING_TIME/1000)
        self._htu_handler.close()

        return

    def read_raw_temp(self):
        """Reads the raw temperature from the sensor."""
        self._htu_handler.open()

        self._htu_handler.send_command((HTU21D_TRIGGERTEMPCMD | self._mode) & 0xFF)
        time.sleep(HTU21D_MAX_MEASURING_TIME/1000)
        msb, lsb, chsum = self._htu_handler.read_bytes(3)

        self._htu_handler.close()

        if self.crc_check(msb, lsb, chsum) is False:
            raise HTU21DException("CRC Exception")

        raw = (msb << 8) + lsb
        raw &= 0xFFFC
        self._logger.debug('Raw temp 0x{0:X} ({1})'.format(raw & 0xFFFF, raw))

        return raw

    def read_raw_humidity(self):
        """Reads the raw relative humidity from the sensor."""
        self._htu_handler.open()

        self._htu_handler.send_command((HTU21D_TRIGGERHUMIDITYCMD | self._mode) & 0xFF)
        time.sleep(HTU21D_MAX_MEASURING_TIME/1000)
        msb, lsb, chsum = self._htu_handler.read_bytes(3)

        self._htu_handler.close()

        if self.crc_check(msb, lsb, chsum) is False:
            raise HTU21DException("CRC Exception")

        raw = (msb << 8) + lsb
        raw &= 0xFFFC
        self._logger.debug('Raw relative humidity 0x{0:04X} ({1})'.format(raw & 0xFFFF, raw))

        return raw

    def read_temperature(self):
        """Gets the temperature in degrees celsius."""
        v_raw_temp = self.read_raw_temp()
        v_real_temp = float(v_raw_temp)/65536 * 175.72
        v_real_temp -= 46.85
        self._logger.debug('Temperature {0:.2f} C'.format(v_real_temp))
        return v_real_temp

    def read_humidity(self):
        """Gets the relative humidity."""
        v_raw_hum = self.read_raw_humidity()
        v_real_hum = float(v_raw_hum)/65536 * 125
        v_real_hum -= 6
        self._logger.debug('Relative Humidity {0:.2f} %'.format(v_real_hum))
        return v_real_hum

    def read_dewpoint(self):
        """Calculates the dew point temperature."""
        # Calculation taken straight from datasheet.
        ppressure = self.read_partialpressure()
        humidity = self.read_humidity()
        den = math.log10(humidity * ppressure / 100) - HTU21D_A
        dew = -(HTU21D_B / den + HTU21D_C)
        self._logger.debug('Dew Point {0:.2f} C'.format(dew))
        return dew

    def read_partialpressure(self):
        """Calculate the partial pressure in mmHg at ambient temperature."""
        v_temp = self.read_temperature()
        v_exp = HTU21D_B / (v_temp + HTU21D_C)
        v_exp = HTU21D_A - v_exp
        v_part_press = 10 ** v_exp
        self._logger.debug('Partial Pressure {0:.2f} mmHg'.format(v_part_press))
        return v_part_press

# vim:ts=4:expandtab
