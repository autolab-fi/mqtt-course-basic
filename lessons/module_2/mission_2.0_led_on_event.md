# Lesson 4: Turn LED On and Report It

## Lesson objective
Turn the real ESP32 LED on and publish one MQTT event.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
This is the simplest physical-output task in the course. Your program directly
sets GPIO 13 high, then publishes an event so the checker can see what your code
claims it did.

Use GPIO 13 for the LED in this course. If you are checking the ESP32 board
layout, these references show where GPIO pins are located:

![ESP32 GPIO reference](https://api.ondroid.org/media/courses/12/images/a0fb72a9f51d47019b0bb4397a3de285.png)

![ESP32 pin labels](https://api.ondroid.org/media/courses/12/images/ab264aaca8a04e60bd1bf4156bae934c.png)

## Lab architecture
Your code runs on the real ESP32. The checker cannot read your local variables,
so your program must publish an MQTT event after changing the LED. That event is
the device-to-checker confirmation for this small task.

![GPIO 13 is set high to turn the LED on, then the ESP32 publishes a LED event.](../../images/lessons/lesson-04-led-on-event.svg)

## MQTT and hardware concepts
`Pin(13, Pin.OUT)` opens GPIO 13 as an output. `led.value(1)` turns the LED on.
The event topic is `ATTEMPT_TOPIC_ROOT + "/event"`. It is used for short reports
about things that happened on the device.

## Assignment
Write a program that:

- creates `Pin(13, Pin.OUT)`
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

## Starter shape

```python
import json
from machine import Pin

led = Pin(13, Pin.OUT)
# TODO: set the LED output high

client = make_mqtt_client()
topic = ATTEMPT_TOPIC_ROOT + "/event"

client.connect()
# TODO: publish {"name": "led", "state": True}
client.disconnect()
```

## Conclusion
You changed a real GPIO output and reported it through MQTT.
