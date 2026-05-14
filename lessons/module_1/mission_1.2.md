# Lesson 2: Publish One JSON Message

## Lesson objective
Connect to MQTT and publish one JSON telemetry message.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
MQTT devices send data by publishing messages to topics. In this lesson the ESP32
will publish one telemetry message to the topic prepared for your attempt.

## Lab architecture
For every submission, the worker creates a unique topic root and injects it into
your program as `ATTEMPT_TOPIC_ROOT`. This keeps your messages separate from other
students and from your previous attempts. The verifier subscribes to your
telemetry topic and waits for the JSON payload from the real ESP32.

## MQTT concepts
`make_mqtt_client()` returns a preconfigured MQTT client for the lab broker. You
call `connect()` before publishing because MQTT messages can only be sent after
the client has an active broker connection. `publish(topic, payload)` sends bytes
to one topic. `json.dumps(...)` turns a Python dictionary into JSON text, and
`.encode()` converts the text topic and payload into bytes for MicroPython's MQTT
client.

The helper uses MicroPython's `umqtt.simple` library. It is intentionally small:
it does not hide the MQTT lifecycle, so your program still needs to connect,
publish or subscribe, poll incoming messages when needed, and disconnect.

`ATTEMPT_TOPIC_ROOT + "/telemetry"` is the device-to-checker channel for simple
status data. Telemetry answers the question: "What is the device reporting now?"

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
