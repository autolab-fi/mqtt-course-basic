import time
from machine import Pin

led = Pin(2, Pin.OUT)

client = make_mqtt_client()
topic = ATTEMPT_TOPIC_ROOT + "/command"


def on_message(topic, message):
    led.value(1)


client.set_callback(on_message)
client.connect()
client.subscribe(topic.encode())

for _ in range(30):
    client.check_msg()
    time.sleep_ms(100)

client.disconnect()
