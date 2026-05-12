# Lesson 6: Control the LED from MQTT

## Lesson objective
Turn the ESP32 LED on or off from a JSON MQTT command.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
This is the first physical IoT control task. The checker sends a JSON command,
your program changes the LED, and then your program publishes an event.

Assume the LED is connected to `GPIO 2`.

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
