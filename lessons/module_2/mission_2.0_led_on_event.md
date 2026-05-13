# Lesson 4: Turn LED On and Report It

## Lesson objective
Turn the real ESP32 LED on and publish one MQTT event.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
This is the simplest physical-output task in the course. Your program directly
sets GPIO 2 high, then publishes an event so the checker can see what your code
claims it did.

## Lab architecture
Your code runs on the real ESP32. The checker cannot read your local variables,
so your program must publish an MQTT event after changing the LED. That event is
the device-to-checker confirmation for this small task.

## MQTT and hardware concepts
`Pin(2, Pin.OUT)` opens GPIO 2 as an output. `led.value(1)` turns the LED on.
The event topic is `ATTEMPT_TOPIC_ROOT + "/event"`. It is used for short reports
about things that happened on the device.

## Assignment
Write a program that:

- creates `Pin(2, Pin.OUT)`
- turns the LED on with `led.value(1)`
- connects to MQTT
- publishes one event to `ATTEMPT_TOPIC_ROOT + "/event"`
- disconnects cleanly

Required event:

```json
{
  "name": "led",
  "state": true
}
```

## Minimal solution shape

```python
import json
from machine import Pin

led = Pin(2, Pin.OUT)
led.value(1)

client = make_mqtt_client()
topic = ATTEMPT_TOPIC_ROOT + "/event"

client.connect()
client.publish(topic.encode(), json.dumps({"name": "led", "state": True}).encode())
client.disconnect()
```

## Conclusion
You changed a real GPIO output and reported it through MQTT.
