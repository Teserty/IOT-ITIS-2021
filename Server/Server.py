import random
import random
import time
import json


from paho.mqtt import client as mqtt_client

broker = 'broker.hivemq.com'
port = 1883
topic1 = "vmk/team_4"
topic2 = "vmk/team_4/commands"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-0'
worker_id = f'python-mqtt-1'
# username = 'emqx'
# password = 'public'

brokerT = 'thingsboard.cloud'
topicTelemetry = 'v1/devices/me/telemetry'
topicRequest = 'v1/devices/me/rpc/request/'
topicResponse = 'v1/devices/me/rpc/response/'
topicRequest = "v1/devices/me/rpc/request/+"
# generate client ID with pub prefix randomly
# username = 'emqx'
# password = 'public'
ACCESS_TOKEN = 'Hj0payDBaIzqWowpoj0U'

def connect_mqtt(id, broker) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(id)
    client.username_pw_set(ACCESS_TOKEN)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


sensors_per = []


def on_message(client, userdata, msg):
    from ast import literal_eval
    import json
    data = literal_eval(msg.payload.decode('utf8'))
    global sensors_per
    sensors_per = data
    print(sensors_per)
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


def subscribe(client: mqtt_client):
    client.subscribe(topic1)
    client.on_message = on_message


def publish(client):
    while True:
        print(sensors_per)
        time.sleep(5)
        for sensor in sensors_per:
            result = client.publish(topicRequest, json.dumps(sensor))



def run():
    import threading
    client = connect_mqtt('0', brokerT)
    client.loop_start()
    thread1 = threading.Thread(target=publish, args=[client])
    thread1.start()
    client = connect_mqtt('2', broker)
    subscribe(client)
    client.loop_forever()


def exec():
    run()
