import smbus
from flask import Flask
import json

DEVICE = 0x23
POWER_DOWN = 0x00
POWER_ON = 0x01
RESET = 0x07
CONTINUOUS_LOW_RES_MODE = 0x13
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
ONE_TIME_LOW_RES_MODE = 0x23

# bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1


def convertToNumber(data):
    result = (data[1] + (256 * data[0])) / 1.2
    return (result)


def readLight(addr=DEVICE):
    # Read data from I2C interface
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(data)


def get_light(time):
    value = readLight()
    x = {"sensorID": "0", "typeSensor": "light", "typeValue": "float", "value": value, "time": str(time)}
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


# sensors_per = [get_light()]#, get_humidity()]
sensors_req = [get_light_status(), get_pomp_status()]
controllers = [set_light(), set_pomp()]
app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    import datetime
    return json.dumps([get_light(datetime.datetime.now()), get_humidity()])


def signals():
    from gpiozero import LED
    red = LED(16)
    green = LED(20)
    blue = LED(21)
    current = red
    import time
    while True:
        val = readLight()
        if val > 20:
            if current is not blue:
                current.off()
                current = blue
                current.on()
        elif val > 60:
            if current is not green:
                current.off()
                current = green
                current.on()
        else:
            if current is not red:
                current.off()
                current = red
                current.on()
        time.sleep(1)


def exec():
    import threading
    thread1 = threading.Thread(target=signals)
    thread1.start()
    app.run(port=5000)
