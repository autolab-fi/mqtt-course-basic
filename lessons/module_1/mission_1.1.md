# Lesson 1: 30-Second MQTT Sandbox

## Lesson objective
Run a tiny MicroPython program on the ESP32 and see what the board prints or publishes.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
This sandbox is for trying code safely before writing a strict lesson solution.
Your program can print text and, if you want, publish MQTT messages. The checker
will run it for up to 30 seconds.

## Assignment
Write a short program that prints one line.

Example:

```python
print("Hello from ESP32")
```

Optional MQTT test:

```python
import json

client = make_mqtt_client()
topic = ATTEMPT_TOPIC_ROOT + "/telemetry"

client.connect()
client.publish(topic.encode(), json.dumps({"name": "sandbox", "value": 1}).encode())
client.disconnect()
```

## Notes
- The sandbox is not about perfect code. It is for testing.
- The program must not need more than 30 seconds.
- If your program waits for messages, use a limited loop such as `for _ in range(30)`.

## Conclusion
You can now run small snippets on the real board and inspect the result.
