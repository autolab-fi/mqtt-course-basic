import json

client = make_mqtt_client()
topic = ATTEMPT_TOPIC_ROOT + "/telemetry"

client.connect()
client.publish(topic.encode(), json.dumps({"name": "status", "value": "online"}).encode())
client.disconnect()
