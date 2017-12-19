# Adafruit_Python_HTU21D
Python Library for the Adafruit HTU21D-F Humidity/Temperature sensor breakout board.

Partially based on the code of the Adafruit_Python_BMP library written by Tony DiCola for Adafruit Industries.

**Warning**:

* ***Python 2.7*** is only partially supported;
* "*Hold Master*" mode is not implemented;
* **Beagle** boards (BeagleBoard, BeagleBone/Black) have not already been tested;
* read/write user reg is not implemented.

## Currently supported platforms
|                  Board | Options                     |
| ---------------------- | --------------------------- |
| Raspberry PI 1 Model B | ***busnum=0***              |
| Raspberry PI 2 Model B | *busnum* default or ***1*** |
| Raspberry PI 3 Model B | *busnum* default or ***1*** |

## Installation

### Setuptools
The following commands install HTU21D library *system wide*:

~~~console
git clone https://github.com/mgaggero/Adafruit_Python_HTU21D.git
cd Adafruit_Python_HTU21D
sudo python setup.py install
~~~

In order to install the library on the user's home directory, a *local installation* that not requires sudo/root privileges, the last command should be:

~~~console
python setup.py install --user
~~~

And the library will be installed in the folder 

~~~console
$HOME/.local/lib/python3.6/site-packages/
~~~

### Pip

The following commands install HTU21D library *system wide*:

~~~console
git clone https://github.com/mgaggero/Adafruit_Python_HTU21D.git
cd Adafruit_Python_HTU21D
sudo pip install .
~~~

In order to install the library on the user's home directory, a *local installation* that not requires sudo/root privileges, the last command should be:

~~~console
pip install . --user
~~~

And the library will be installed in the folder 

~~~console
$HOME/.local/lib/python3.6/site-packages/
~~~


## Permissions and privileges
Accessing **I2C** devices usually requires root privileges or privileged group membership. These can be obtained with:

* the use of `sudo` to run the program;
* adding the user that runs the program to the I2C's device owning group;
* creating an '**i2c**' group, assigning the i2c device to it and adding the user to that group.

### Creation of the 'i2c' group
~~~console
sudo groupadd -r i2c        # creates the 'i2c' group as a 'system' group
sudo chgrp i2c /dev/i2c*    # changes group ownership of the i2c device files
sudo chmod g+rw /dev/i2c*   # allow owning group to read/write to the devices
sudo usermod -aG i2c $USER  # add the current user to the 'i2c' group
~~~
Logout and re-login.

## Usage
~~~python
>>> from Adafruit_HTU21D.HTU21D import HTU21D

>>> h = HTU21D()

>>> h.read_temperature()
24.117971191406248

>>> h.read_humidity()
35.1224365234375

>>> h.read_dewpoint()
7.783974941964999

>>> h.reset()
~~~

## Troubleshooting
### ArchLinux
Before reporting any bugs or issues, make sure that:

* the file */boot/config.txt* contains the line  
`dtparam=i2c_arm=on`  
Uncomment if necessary and reboot the board.


* kernel module  
`i2c-dev`  
is loaded. Otherwise, load it with:  
`sudo modprobe i2c-dev`


