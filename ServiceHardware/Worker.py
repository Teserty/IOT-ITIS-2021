import smbus
import requests
from flask import Flask, url_for
from markupsafe import escape
import threading
import time
import json
from paho.mqtt import client as mqtt_client


# Define some constants from the datasheet

DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  # Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)



broker = 'broker.hivemq.com'
port = 1883
topic1 = "vmk/team_4"
topic2 = "vmk/team_4/commands"
# generate client ID with pub prefix randomly
client_id = 'python-mqtt-0'
worker_id = 'python-mqtt-1'


def get_light():
    value=readLight()
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


from gpiozero import Button
button = Button(6)
a = False
def u(client):
   while True:
        if button.is_pressed:
            client.publish(topic1, json.dumps(get_light()))
            time.sleep(1)



def publish():
    while True:
        time.sleep(5)
        requests.post("localhost:5001", json.dumps(sensors_per))



app = Flask(__name__)


@app.route('/')
def hello_world():
    publish()


def exec():
    publisher = threading.Thread(target=publish)
    publisher.start()
    app.run()

