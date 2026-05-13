# Lesson 8: Parse a JSON Command

## Lesson objective
Receive one MQTT command and parse its JSON payload.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
MQTT sends bytes. Most IoT commands are JSON text inside those bytes. Your code
must decode the message and then use `json.loads(...)` to turn it into a Python
dictionary.

## Lab architecture
The worker acts like a small control application. After your ESP32 publishes
`command_ready`, the worker publishes a JSON command to your attempt command
topic. Your program reads that command on the real board, parses it, and reports
what it understood by publishing an event.

## MQTT concepts
MQTT does not know that a payload is JSON. It only transports bytes. That is why
the callback receives a byte string. `message.decode()` converts bytes to text,
and `json.loads(...)` converts the JSON text into a Python dictionary so your code
can read fields such as `target`, `action`, and `value`.

An event topic is used for facts about something that happened. In this lesson,
the event means: "the device received and parsed a command."

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
