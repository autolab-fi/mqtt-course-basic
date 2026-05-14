import json
import time
from machine import Pin

led = Pin(13, Pin.OUT)
client = make_mqtt_client()
command_topic = ATTEMPT_TOPIC_ROOT + "/command"
telemetry_topic = ATTEMPT_TOPIC_ROOT + "/telemetry"
event_topic = ATTEMPT_TOPIC_ROOT + "/event"
state_topic = ATTEMPT_TOPIC_ROOT + "/state"
state = {"value": False, "done": False}


def publish_led_state():
    client.publish(
        state_topic.encode(),
        json.dumps({"target": "led", "state": state["value"]}).encode(),
    )
    client.publish(
        event_topic.encode(),
        json.dumps({"name": "led", "event": "changed", "state": state["value"]}).encode(),
    )


def on_message(topic, message):
    command = json.loads(message.decode())
    action = command.get("action")
    if command.get("target") != "led":
        return
    if action == "on":
        state["value"] = True
    elif action == "off":
        state["value"] = False
    elif action == "toggle":
        state["value"] = not state["value"]
    else:
        return
    led.value(1 if state["value"] else 0)
    publish_led_state()
    state["done"] = True


client.set_callback(on_message)
client.connect()
client.subscribe(command_topic.encode())
client.publish(telemetry_topic.encode(), json.dumps({"name": "protocol_ready", "value": 1}).encode())

for _ in range(30):
    client.check_msg()
    if state["done"]:
        break
    time.sleep_ms(100)

client.disconnect()
