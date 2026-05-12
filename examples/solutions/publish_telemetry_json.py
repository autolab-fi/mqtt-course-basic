import json

client = make_mqtt_client()
topic = ATTEMPT_TOPIC_ROOT + "/telemetry"

client.connect()
client.publish(topic.encode(), json.dumps({"name": "hello", "value": 1}).encode())
client.disconnect()
