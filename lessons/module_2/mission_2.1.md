# Lesson 4: Subscribe and Poll Commands

## Lesson objective
Subscribe to an MQTT command topic and poll for incoming messages.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
IoT devices often listen for commands from another program. In MicroPython with
`umqtt.simple`, a common beginner pattern is:

- subscribe to a topic
- set a callback
- call `check_msg()` inside a short loop

## Assignment
Write a program that:

- connects to MQTT
- subscribes to `ATTEMPT_TOPIC_ROOT + "/command"`
- publishes ready telemetry to `ATTEMPT_TOPIC_ROOT + "/telemetry"`
- polls messages with `check_msg()` for a limited time
- disconnects cleanly

Required ready telemetry:

```json
{
  "name": "command_ready",
  "value": 1
}
```

## Notes
- Use a limited loop such as `for _ in range(30)`.
- Do not use an endless `while True` loop in this course task.

## Conclusion
You can now subscribe to a command topic and give MQTT time to deliver messages.
