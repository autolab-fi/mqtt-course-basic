import json
from machine import Pin

leds = [Pin(2, Pin.OUT), Pin(4, Pin.OUT)]
for led in leds:
    led.value(1)

client = make_mqtt_client()
topic = ATTEMPT_TOPIC_ROOT + "/event"

client.connect()
client.publish(topic.encode(), json.dumps({"name": "led", "state": True}).encode())
client.disconnect()
