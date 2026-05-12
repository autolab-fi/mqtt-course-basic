import json
import time

client = make_mqtt_client()
command_topic = ATTEMPT_TOPIC_ROOT + "/command"
telemetry_topic = ATTEMPT_TOPIC_ROOT + "/telemetry"


def on_message(topic, message):
    print("received", topic, message)


client.set_callback(on_message)
client.connect()
client.subscribe(command_topic.encode())
client.publish(telemetry_topic.encode(), json.dumps({"name": "command_ready", "value": 1}).encode())

for _ in range(30):
    client.check_msg()
    time.sleep_ms(100)

client.disconnect()
