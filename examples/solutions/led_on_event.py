import json
from machine import Pin

led = Pin(13, Pin.OUT)
led.value(1)

client = make_mqtt_client()
topic = ATTEMPT_TOPIC_ROOT + "/event"

client.connect()
client.publish(topic.encode(), json.dumps({"name": "led", "state": True}).encode())
client.disconnect()
