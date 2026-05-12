# Lesson 5: Parse a JSON Command

## Lesson objective
Receive one MQTT command and parse its JSON payload.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
MQTT sends bytes. Most IoT commands are JSON text inside those bytes. Your code
must decode the message and then use `json.loads(...)` to turn it into a Python
dictionary.

## Assignment
Write a program that:

- subscribes to `ATTEMPT_TOPIC_ROOT + "/command"`
- publishes `command_ready` telemetry
- receives a JSON command
- parses the command with `json.loads(...)`
- publishes an event containing the parsed action

Checker command:

```json
{
  "target": "led",
  "action": "set",
  "value": true
}
```

Required event:

```json
{
  "name": "command",
  "event": "parsed",
  "action": "set"
}
```

## Conclusion
You can now read a structured command from MQTT.
