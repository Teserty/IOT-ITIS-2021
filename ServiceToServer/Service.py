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


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


def subscribe(client: mqtt_client):
    client.subscribe(topic1)
    client.on_message = on_message


def publish(client):
    return 0



def run():
    client = connect_mqtt('0')
    client.loop_start()
    client = connect_mqtt('2')
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
