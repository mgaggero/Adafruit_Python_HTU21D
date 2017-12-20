## Adafruit_Python_HTU21D

Python Library for the Adafruit HTU21D-F Humidity/Temperature sensor breakout board.

It does not use any other library than the standard ones usually provided with the OS Python distribution.

HTU21D specifications are based on the [Te MEAS Datasheet](http://www.te.com/commerce/DocumentDelivery/DDEController?Action=showdoc&DocId=Data+Sheet%7FHPC199_6%7FA6%7Fpdf%7FEnglish%7FENG_DS_HPC199_6_A6.pdf%7FHPP845E031).

Partially based on the code of the Adafruit_Python_BMP library written by Tony DiCola for Adafruit Industries.

**Warning**:

* ***Python 2.7*** is only partially supported;
* "*Hold Master*" mode is not implemented;
* **Beagle** boards (BeagleBoard, BeagleBone/Black) have not already been tested;
* read/write user reg is not implemented.

[toc]

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

### OS-specific Installations
### ArchLinux
ArchLinux default for Raspberry PI is to not load any I2C device and not create I2C owning group.  
So for an Arch Linux fresh install, it has to do:

1. enable the i2c hardware peripheral in the kernel;
1. enable *i2c-dev* kernel module load at boot;
1. create the *i2c*system group;
1. instruct *UDEV* to change owner and permissions to the *i2c device*;
1. [optionally] add users to *i2c* group.

In the file */boot/config.txt* add or uncomment if present commented, the line:  
`dtparam=i2c_arm=on`

Create the file */etc/modules-load.d/i2c-dev.conf*:  

~~~console
sudo sh -c "echo i2c-dev > /etc/modules-load.d/i2c-dev.conf"
~~~

Create the '*i2c*' system group:

~~~console
sudo groupadd -r i2c
~~~

Create the */etc/udev/rules.d/90-i2c_dev.rules* file with the contents:

~~~udev
KERNEL=="i2c-[0-9]*", GROUP="i2c"', MODE="0660"
~~~

[Optional] Add the current user to the '*i2c*' group:

~~~console
sudo usermod -aG i2c $USER
~~~

Reboot and login.

(Based on: [fabb on StackExchange](https://raspberrypi.stackexchange.com/questions/4468/i2c-group-on-arch),
[JPB-HK on Raspberrypi.Org Forum](https://www.raspberrypi.org/forums/viewtopic.php?p=238003#p238003))

## Permissions and privileges
Accessing **I2C** devices usually requires root privileges or privileged group membership. These can be obtained with:

* the use of `sudo` to run the program;
* adding the user that runs the program to the I2C's device owning group, if exists;
* creating an '**i2c**' group, assigning the i2c device to it and adding the user to that group, see [ArchLinux](#archlinux)

### Creation of the 'i2c' group: quick and dirty way
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
### FileNotFoundError: [Errno 2] No such file or directory: '/dev/i2c-X'
**The *i2c* device is missing in the */dev/***

Check that the *i2c-dev* module is loaded with the command:

~~~console
lsmod | grep i2c_dev
~~~

otherwise, load the kernel module:

~~~console
sudo modprobe i2c-dev
~~~

Once loaded, the check should return:

~~~console
$ lsmod | grep i2c_dev
i2c_dev                 6673  0
~~~

### PermissionError: [Errno 13] Permission denied: '/dev/i2c-X'
**The current user is not allow to access the *i2c* device.**

See [Permissions and privileges](#Permissions-and-privileges#).

## Bugs and Issues
Before reporting any bugs or issues, make sure that:

* the file */boot/config.txt* contains the line  
`dtparam=i2c_arm=on`  
Uncomment if necessary and reboot the board.


* kernel module  
`i2c-dev`  
is loaded. Otherwise, load it with:  
`sudo modprobe i2c-dev`
