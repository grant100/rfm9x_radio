import logging
from logging.handlers import SysLogHandler
import platform
from flask import Flask, request
from flask_cors import CORS

import setproctitle
import threading, argparse, sys
from queue import Queue, Empty

from lora_device.device import Radio

setproctitle.setproctitle('rfm9x')
parser = argparse.ArgumentParser(description='RFM9x Radio')
parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='enable debug output')

args = parser.parse_args()
logger = logging.getLogger()

if args.debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

address = '/dev/log'
if platform.system() == 'Darwin':
    address = '/var/run/syslog'

logger.addHandler(SysLogHandler(address=address))
logger.addHandler(logging.StreamHandler())
app = Flask(__name__)
CORS(app)

sensor_data = None
sensor_queue = Queue(maxsize=1)
radio = Radio(sensor_queue=sensor_queue)


@app.route('/sensor', methods=['POST'])
def sensor():
    try:
        sensor_data = sensor_queue.get(timeout=5)
    except Empty:
        return "error"
    sensor_queue.task_done()
    return sensor_data.to_json()


if __name__ == '__main__':
    radio.start()
    app.run(port=8081, host='0.0.0.0')
