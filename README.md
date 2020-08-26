#RFM9x RADIO

## Setup LoRa Device (Pi Zero)

Install CircuitPython Libraries

Setup PI with this:
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

## Enable I2C and SPI (Once per PI)
Ref: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

```
  sudo apt-get install -y python-smbus
  sudo apt-get install -y i2c-tools
  sudo raspi-config
  
  Interfaces->I2C->enable
  Interfaces->SPI->enable
```
Reboot the PI

## Enable 
Install python libraries:
```
  sudo pip3 install adafruit-circuitpython-ssd1306
  sudo pip3 install adafruit-circuitpython-framebuf
  sudo pip3 install adafruit-circuitpython-rfm9x
```

## Setup Feather M0 with BME280 Device (Microcontroller)

Flash circuit python on to Feather M0 (*bossac* must be installed):

```

  ls /dev/cu.* // list connected devices
  bossac -p /dev/cu.usbmodem143101 -e -w -v -R --offset=0x2000 firmware.bin
  
```

## Notes:

Must run with `python3` or this error is raised:

```
Traceback (most recent call last):
  File "lora_device/radio_check.py", line 8, in <module>
    import busio
ModuleNotFoundError: No module named 'busio'
```
