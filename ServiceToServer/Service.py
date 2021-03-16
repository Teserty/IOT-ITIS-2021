import requests
import time
import json
from paho.mqtt import client as mqtt_client

broker = 'broker.hivemq.com'
port = 1883
client_id = f'0'
worker_id = f'1'
sensors_per=[]
subscriber = mqtt_client.Client('0')
publisher = mqtt_client.Client('1')


def publish():
    val = requests.post("http://localhost:5000/")
    global sensors_per
    sensors_per = val
    print(val)
    return val.json()


def publish_loop(client):
    print("Publish loop")
    while True:
        client.publish("vmk/team_4/r", json.dumps(publish()))
        time.sleep(5)


def alert_loop():
    while True:
        val = publish()
        if val[0].get('value') < 10:
            publisher.publish("vmk/team_4/r", json.dumps([{"action": 'alert'}]))
            publisher.publish("vmk/team_4/r", json.dumps(publish()))
            time.sleep(20)
        time.sleep(2)


def subscribe(client):
    def on_message(client, userdata, msg):
        print(msg)
        publisher.publish("vmk/team_4/r", json.dumps(publish()))
    client.subscribe("vmk/team_4/c")
    client.on_message = on_message


def run():
    print("Started")
    import threading
    subscriber.connect(broker, port)
    publisher.connect(broker, port)
    subscribe(subscriber)
    thread1 = threading.Thread(target=subscriber.loop_forever)
    thread1.start()
    thread2 = threading.Thread(target=alert_loop)
    thread2.start()
    publisher.loop_start()
    publish_loop(publisher)


def exec():
    run()


if __name__ == "__main__":
    exec()
