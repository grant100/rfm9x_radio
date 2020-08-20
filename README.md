#RFM9x RADIO

## Setup LoRa Device (Pi Zero)

Install CircuitPython Libraries

Setup PI with this:
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

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
