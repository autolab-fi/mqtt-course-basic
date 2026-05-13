# Lesson 6: Minimal LED Command Listener

## Lesson objective
Receive one MQTT command and turn the LED on.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
This is the smallest command-listener task. The checker sends a command to your
attempt command topic. Your program subscribes to that topic, polls MQTT for a
short time, and turns the LED on when any command message arrives.

## Lab architecture
The worker starts your program and then publishes a checker command to
`ATTEMPT_TOPIC_ROOT + "/command"`. Your ESP32 receives the message through MQTT.
For this minimal lesson, the important part is learning the subscribe/callback
shape before parsing JSON commands.

## MQTT concepts
`set_callback(...)` tells the MQTT client which function should handle incoming
messages. `subscribe(...)` tells the broker which topic you want. `check_msg()`
lets the MicroPython MQTT client process waiting messages and call your callback.

## Assignment
Write a program that:

- creates `Pin(2, Pin.OUT)`
- creates an MQTT client
- sets a callback function
- connects and subscribes to `ATTEMPT_TOPIC_ROOT + "/command"`
- calls `check_msg()` inside a limited loop
- turns the LED on in the callback
- disconnects cleanly

Checker command:

```json
{
  "target": "led",
  "action": "on"
}
```

## Minimal solution shape

```python
import time
from machine import Pin

led = Pin(2, Pin.OUT)

client = make_mqtt_client()
topic = ATTEMPT_TOPIC_ROOT + "/command"


def on_message(topic, message):
    led.value(1)


client.set_callback(on_message)
client.connect()
client.subscribe(topic.encode())

for _ in range(30):
    client.check_msg()
    time.sleep_ms(100)

client.disconnect()
```

## Conclusion
You have received a command over MQTT and used it to control real hardware.
