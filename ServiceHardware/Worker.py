#import smbus
import requests
from flask import Flask, url_for
import threading
import time
import json


DEVICE     = 0x23
POWER_DOWN = 0x00
POWER_ON   = 0x01
RESET      = 0x07
CONTINUOUS_LOW_RES_MODE = 0x13
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
#bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

#def convertToNumber(data):
#  result=(data[1] + (256 * data[0])) / 1.2
#  return (result)
#
#def readLight(addr=DEVICE):
#  # Read data from I2C interface
#  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
#  return convertToNumber(data)
#

def get_light():
    value=0#readLight()
    x = {"sensorID":"0", "typeSensor":"light", "typeValue":"float", "value": value}
    return x


def get_humidity():
    value = 0
    x = {"sensorID": "1", "typeSensor": "humidity", "typeValue": "float", "value": value}
    return x


def get_light_status():
    value = False
    x = {"sensorID": "2", "typeSensor": "light_status", "typeValue": "boolean", "value": value}
    return x


def get_pomp_status():
    value = False
    x = {"sensorID": "3", "typeSensor": "pomp_status", "typeValue": "boolean", "value": value}
    return x


def set_light():
    return 0


def set_pomp():
    return 0


sensors_per = [get_light(), get_humidity()]
sensors_req = [get_light_status(), get_pomp_status()]
controllers = [set_light(), set_pomp()]



def publish():
    while True:
        time.sleep(5)
        requests.post("http://localhost:5001/", json.dumps(sensors_per))


app = Flask(__name__)


@app.route('/')
def hello_world():
    publish()


def exec():
    publisher = threading.Thread(target=publish)
    publisher.start()
    app.run(port=5000)
