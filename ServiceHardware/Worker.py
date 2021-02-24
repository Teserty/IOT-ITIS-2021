import random
import time
import json

from paho.mqtt import client as mqtt_client
import json

broker = 'broker.emqx.io'
broker1 = 'broker.emqx.io.worker'
broker2 = 'broker.emqx.io.service'
port = 1883
topic1 = "/python/mqtt/sensors"
topic2 = "/python/mqtt/commands"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-0'
worker_id = f'python-mqtt-1'


def get_light():
    value = 0
    x = {"sensorID":"0", "typeSensor":"light", "typeValue":"float", "value": value}
    return x


def get_humidity():
    value = 0
    x = {"sensorID": "1", "typeSensor": "humidity", "typeValue": "float", "value": value}
    return x


def get_light_status():
    value = False
    x = {"sensorID": "2", "typeSensor": "temperature", "typeValue": "boolean", "value": value}
    return x


def get_pomp_status():
    value = False
    x = {"sensorID": "3", "typeSensor": "temperature", "typeValue": "boolean", "value": value}
    return x


def set_light():
    return 0


def set_pomp():
    return 0


sensors_per = [get_light(), get_humidity()]
sensors_req = [get_light_status(), get_pomp_status()]
controllers = [set_light(), set_pomp()]


def connect_mqtt(id) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    while True:
        time.sleep(5)
        for sensor in sensors_per:
            result = client.publish(topic1, json.dumps(sensor))
            status = result[0]


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic2)
    client.on_message = on_message


def run():
    client = connect_mqtt(worker_id)
    subscribe(client)
    client = connect_mqtt(client_id)
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()