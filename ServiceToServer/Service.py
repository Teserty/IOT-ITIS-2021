import requests as rq
from flask import Flask, url_for
from markupsafe import escape
import threading
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


def connect_mqtt(id):
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


sensors_per=[]


def publish(client):
    while True:
        time.sleep(5)
        result = client.publish(topic1, json.dumps(sensors_per))



def subscribe(client):
    def on_message(client, userdata, msg):
        print(msg.payload)

    client.subscribe(topic2)
    client.on_message = on_message


import threading


def run():
    client = connect_mqtt(worker_id)
    subscribe(client)
    client = connect_mqtt(client_id)
    client.loop_start()
    th = threading.Thread(target=publish, args=[client])
    th.start()


app = Flask(__name__)

from flask import request, jsonify


@app.route('/', methods=['POST'])
def hello_world():
    from ast import literal_eval
    import json
    data = literal_eval(request.data.decode('utf8'))
    global sensors_per
    sensors_per = data
    #print(data)
    #s = json.dumps(data, indent=4, sort_keys=True)
    #print(s)
    return "200"


def exec():
    run()
    app.run(port=5001)
