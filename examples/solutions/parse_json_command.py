import json
import time

client = make_mqtt_client()
command_topic = ATTEMPT_TOPIC_ROOT + "/command"
telemetry_topic = ATTEMPT_TOPIC_ROOT + "/telemetry"
event_topic = ATTEMPT_TOPIC_ROOT + "/event"
parsed = {"done": False}


def on_message(topic, message):
    command = json.loads(message.decode())
    payload = {
        "name": "command",
        "event": "parsed",
        "action": command.get("action"),
    }
    client.publish(event_topic.encode(), json.dumps(payload).encode())
    parsed["done"] = True


client.set_callback(on_message)
client.connect()
client.subscribe(command_topic.encode())
client.publish(telemetry_topic.encode(), json.dumps({"name": "command_ready", "value": 1}).encode())

for _ in range(30):
    client.check_msg()
    if parsed["done"]:
        break
    time.sleep_ms(100)

client.disconnect()
