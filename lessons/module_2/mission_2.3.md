# Lesson 6: Control the LED from MQTT

## Lesson objective
Turn the ESP32 LED on or off from a JSON MQTT command.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
This is the first physical IoT control task. The checker sends a JSON command,
your program changes the LED, and then your program publishes an event.

Assume the LED is connected to `GPIO 2`.

## Lab architecture
This lesson closes the loop between software and physical hardware. The worker
publishes a command, the ESP32 receives it over MQTT, your code changes a GPIO
pin, and the board publishes an event back. The verifier checks the MQTT event,
and the lab may also show the real board through the video stream.

## MQTT and hardware concepts
`machine.Pin(2, Pin.OUT)` gives your code control over GPIO 2 as an output pin.
Calling `led.value(1)` drives the pin high, and `led.value(0)` drives it low.
On this board, that controls the visible LED.

The MQTT command contains the desired state. Your code should not just publish a
success message; it should first apply the command to the hardware and then
publish an event describing the change. That event is the device's confirmation
that it acted on the command.

## Assignment
Write a program that:

- reads broker settings through `make_mqtt_client()`
- subscribes to `ATTEMPT_TOPIC_ROOT + "/command"`
- publishes `led_ready` telemetry
- waits for one JSON LED command
- turns the LED on or off using `machine.Pin`
- publishes one LED change event
- disconnects cleanly

Checker command:

```json
{
  "target": "led",
  "action": "set",
  "value": true
}
```

Required ready telemetry:

```json
{
  "name": "led_ready",
  "value": 1
}
```

Required event:

```json
{
  "name": "led",
  "event": "changed",
  "state": true
}
```

## Conclusion
You have controlled real hardware through MQTT.
