"""
Adafruit IO LoRa Gateway

Learn Guide: https://learn.adafruit.com/multi-device-lora-temperature-network

by Brent Rubell for Adafruit Industries
"""
import time
import threading
import logging
import busio
import board
from digitalio import DigitalInOut, Direction, Pull
import adafruit_ssd1306
import adafruit_rfm9x

from queue import Queue
import json

logger = logging.getLogger().getChild(__name__)


class SensorData:
    def __init__(self, device_id, temperature, humidity, pressure):
        self.device_id = device_id
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

    def to_json(self):
        json_dict = {'device_id': self.device_id, 'temperature': self.temperature, 'humidity': self.humidity,
                     'pressure': self.pressure}
        return json.loads(json_dict)

    def __repr__(self):
        return "SensorData(<device_id=%s, temperature=%s, humidity=%s, pressure=%s>)" % (
            self.device_id, self.temperature, self.humidity, self.pressure)


class Radio(threading.Thread):
    def __init__(self, sensor_queue: Queue, frequency=905.5):
        super().__init__()
        self.stop = False

        self.rfm9x = None
        self.display = None
        self.current_packet = None
        self.previous_packet = None
        self.sensor_queue = sensor_queue
        self.frequency = frequency
        self._setup()

    def _setup(self):
        btnA = DigitalInOut(board.D5)
        btnA.direction = Direction.INPUT
        btnA.pull = Pull.UP

        btnB = DigitalInOut(board.D6)
        btnB.direction = Direction.INPUT
        btnB.pull = Pull.UP

        btnC = DigitalInOut(board.D12)
        btnC.direction = Direction.INPUT
        btnC.pull = Pull.UP

        i2c = busio.I2C(board.SCL, board.SDA)

        self.display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x3c)
        self.display.fill(0)
        self.display.show()
        # width = self.display.width
        # height = self.display.height

        CS = DigitalInOut(board.CE1)
        RESET = DigitalInOut(board.D25)
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        self.rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, self.frequency)

    def int_to_float(self, pkt_val_1, pkt_val_2, pkt_val_3=None):
        """Convert packet data to float.
        """
        if pkt_val_3 is None:
            float_val = pkt_val_1 << 8 | pkt_val_2
        else:
            float_val = pkt_val_1 << 16 | pkt_val_2 << 8 | pkt_val_3
        return float_val / 100

    def run(self) -> None:

        while not self.stop:
            packet = None
            # draw a box to clear the image
            self.display.fill(0)
            self.display.text('BME 280 Sensor', 0, 0, 1)

            # check for packet rx
            self.current_packet = self.rfm9x.receive()
            if packet is None or self.previous_packet:
                self.display.show()
                self.display.text('- Waiting for PKT -', 10, 20, 1)
            else:
                self.previous_packet = packet

                temp_val = self.int_to_float(packet[1], packet[2])
                humid_val = self.int_to_float(packet[3], packet[4])
                pres_val = self.int_to_float(packet[5], packet[6], packet[7])

                sensor_data = SensorData(device_id=packet[0], temperature=temp_val, humidity=humid_val,
                                         pressure=pres_val)
                logger.debug("recieved packet: %s", sensor_data)
                time.sleep(1)

                if not self.sensor_queue.empty():
                    self.sensor_queue.get_nowait()
                    self.sensor_queue.task_done()

                self.sensor_queue.put(sensor_data)

            self.display.show()

    def stop(self):
        self.stop = True
