from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(
    name                  = 'Adafruit_HTU21D',
    version               = '0.1.0',
    author                = 'Massimo Gaggero',
    author_email          = 'massimo.gaggero@crs4.it',
    description           = 'Library for accessing the HTU21D-F humidity and temperature sensor on a Raspberry Pi or Beaglebone Black.',
    license               = 'MIT',
    url                   = 'https://github.com/mgaggero/Adafruit_Python_HTU21D/',
    dependency_links      = ['https://github.com/adafruit/Adafruit_Python_GPIO/tarball/master#egg=Adafruit-GPIO-0.6.5'],
    install_requires      = ['Adafruit-GPIO>=0.6.5'],
    packages              = find_packages()
)