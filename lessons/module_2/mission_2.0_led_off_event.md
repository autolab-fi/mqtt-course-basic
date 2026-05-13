# Lesson 5: Turn LED Off and Report It

## Lesson objective
Turn the real ESP32 LED off and publish one MQTT event.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
This task is the same physical-output pattern as the previous lesson, but the
GPIO value is different. You will drive the LED pin low and report `state: false`.

## Lab architecture
The worker uploads your code to the ESP32 and subscribes to your attempt event
topic. Your code changes the LED and publishes one event. The verifier checks the
MQTT event from the real board.

## MQTT and hardware concepts
`led.value(0)` drives GPIO 2 low, turning the LED off on this board. The JSON
boolean `false` becomes Python `False` in your dictionary before `json.dumps(...)`
converts it to JSON text.

## Assignment
Write a program that:

- creates `Pin(2, Pin.OUT)`
- turns the LED off with `led.value(0)`
- connects to MQTT
- publishes one event to `ATTEMPT_TOPIC_ROOT + "/event"`
- disconnects cleanly

Required event:

```json
{
  "name": "led",
  "state": false
}
```

## Minimal solution shape

```python
import json
from machine import Pin

led = Pin(2, Pin.OUT)
led.value(0)

client = make_mqtt_client()
topic = ATTEMPT_TOPIC_ROOT + "/event"

client.connect()
client.publish(topic.encode(), json.dumps({"name": "led", "state": False}).encode())
client.disconnect()
```

## Conclusion
You can now set the LED both on and off from code running on the ESP32.
