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

from setuptools import setup, find_packages

setup(
    name                  = 'Adafruit_HTU21D',
    version               = '1.0.0',
    author                = 'Massimo Gaggero',
    author_email          = 'massimo.gaggero@crs4.it',
    description           = 'Library for accessing the HTU21D-F humidity and temperature sensor on a Raspberry Pi or Beaglebone Black.',
    license               = 'MIT',
    platforms             = ["Linux"],
    url                   = 'https://github.com/mgaggero/Adafruit_Python_HTU21D/',
    packages              = find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
        'Topic :: Home Automation',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Hardware :: Hardware Drivers',
        ],

)
