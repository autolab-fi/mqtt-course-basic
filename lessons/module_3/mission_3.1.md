# Lesson 7: LED State Protocol

## Lesson objective
Implement a tiny IoT command protocol for one LED.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
A real device usually supports more than one command. In this final beginner
task, your ESP32 supports three LED actions:

- `on`
- `off`
- `toggle`

After the command, the device reports the final state.

## Assignment
Write a program that:

- subscribes to `ATTEMPT_TOPIC_ROOT + "/command"`
- publishes `protocol_ready` telemetry
- accepts JSON commands with `action`
- supports `on`, `off`, and `toggle`
- publishes the final LED state to `ATTEMPT_TOPIC_ROOT + "/state"`
- publishes a LED event to `ATTEMPT_TOPIC_ROOT + "/event"`

Example checker command:

```json
{
  "target": "led",
  "action": "toggle"
}
```

Required final state:

```json
{
  "target": "led",
  "state": true
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
You have built a small MQTT device protocol with command input and state output.
