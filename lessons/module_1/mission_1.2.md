# Lesson 2: Publish One JSON Message

## Lesson objective
Connect to MQTT and publish one JSON telemetry message.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
MQTT devices send data by publishing messages to topics. In this lesson the ESP32
will publish one telemetry message to the topic prepared for your attempt.

## Assignment
Write a program that:

- creates an MQTT client with `make_mqtt_client()`
- connects to the broker
- publishes one JSON message to `ATTEMPT_TOPIC_ROOT + "/telemetry"`
- disconnects cleanly

Required payload:

```json
{
  "name": "hello",
  "value": 1
}
```

## Example shape

```python
import json

client = make_mqtt_client()
topic = ATTEMPT_TOPIC_ROOT + "/telemetry"

client.connect()
client.publish(topic.encode(), json.dumps({"name": "hello", "value": 1}).encode())
client.disconnect()
```

## Conclusion
You have sent your first device telemetry message through MQTT.
