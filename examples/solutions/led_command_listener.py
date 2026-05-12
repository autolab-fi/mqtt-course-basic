import json
import time
from machine import Pin

led = Pin(2, Pin.OUT)
client = make_mqtt_client()
command_topic = ATTEMPT_TOPIC_ROOT + "/command"
telemetry_topic = ATTEMPT_TOPIC_ROOT + "/telemetry"
event_topic = ATTEMPT_TOPIC_ROOT + "/event"
handled = {"done": False}


def on_message(topic, message):
    command = json.loads(message.decode())
    if command.get("target") == "led" and command.get("action") == "set":
        state = bool(command.get("value"))
        led.value(1 if state else 0)
        payload = {"name": "led", "event": "changed", "state": state}
        client.publish(event_topic.encode(), json.dumps(payload).encode())
        handled["done"] = True


client.set_callback(on_message)
client.connect()
client.subscribe(command_topic.encode())
client.publish(telemetry_topic.encode(), json.dumps({"name": "led_ready", "value": 1}).encode())

for _ in range(30):
    client.check_msg()
    if handled["done"]:
        break
    time.sleep_ms(100)

client.disconnect()
